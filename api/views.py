from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User, Assignment
from .serializers import UserSerializer, AssignmentSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

# Register User
@api_view(['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([AllowAny])  
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)  # Create or get existing token
        return Response({"token": token.key}, status=status.HTTP_200_OK)  # Return the token
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Upload assignment
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_assignment(request):
    data = {
        'user': request.user.id,
        'task': request.data.get('task'),
        'admin': request.data.get('admin_id'),
    }
    serializer = AssignmentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get all admins
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_admins(request):
    admins = User.objects.filter(is_admin=True)
    serializer = UserSerializer(admins, many=True)
    return Response(serializer.data)

# Admin: View assignments tagged to the admin
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_assignments(request):
    if request.user.is_admin:
        assignments = Assignment.objects.filter(admin=request.user)
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)
    return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

# Admin: Accept an assignment
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_assignment(request, id):
    try:
        assignment = Assignment.objects.get(id=id, admin=request.user)
        assignment.status = 'accepted'
        assignment.save()
        return Response({"message": "Assignment accepted"}, status=status.HTTP_200_OK)
    except Assignment.DoesNotExist:
        return Response({"error": "Assignment not found"}, status=status.HTTP_404_NOT_FOUND)

# Admin: Reject an assignment
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_assignment(request, id):
    try:
        assignment = Assignment.objects.get(id=id, admin=request.user)
        assignment.status = 'rejected'
        assignment.save()
        return Response({"message": "Assignment rejected"}, status=status.HTTP_200_OK)
    except Assignment.DoesNotExist:
        return Response({"error": "Assignment not found"}, status=status.HTTP_404_NOT_FOUND)
