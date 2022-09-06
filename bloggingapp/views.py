from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from knox.models import AuthToken
from .serializers import *
from .models import *
from django.db.models import Q
import json
from django.http import HttpResponse, JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.


@api_view(['GET','POST'])
def register(request):
    if request.method == 'GET':
        shipments = User.objects.all()
        serializer = RegisterSerializer(shipments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully registered"
            data['email'] = user.email
            data['username'] = user.username
            token = AuthToken.objects.create(user)[1]
            data['token'] = token
            data['password'] = user.password
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.validated_data
            data['username'] = user.username
            data['password'] = user.password
            token = AuthToken.objects.create(user)[1]
            data['token'] = token
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','POST'])
# def uploadImage(request):
#     if request.method == 'GET':
#         shipments = Image.objects.all()
#         serializer = ImageSerializer(shipments, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ImageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def changePassword(request):

    if request.method == 'PUT':

        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not request.user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            elif serializer.data.get("old_password") == serializer.data.get("new_password"):
                return Response({"old_password": ["new password cannot be same"]}, status=status.HTTP_400_BAD_REQUEST)
            request.user.set_password(serializer.data.get("new_password"))
            request.user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def createBlog(request):
    if request.method == 'GET':
        shipments = CreateBlog.objects.all()
        serializer = CreateBlogSerializer(shipments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CreateBlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def reportBlog(request):
    if request.method == 'GET':
        shipments = Report.objects.all()
        serializer = ReportSerializer(shipments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unSaveBlog(request,blog_id):
    try:
        blog = CreateBlog.objects.get(blog_id = blog_id)
        user = User.objects.get(id = request.user.id)
        user.liked_list.remove(blog)
        return Response(status=status.HTTP_201_CREATED)
    except CreateBlog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def search(request):
#     if request.method == 'GET':
#         try:
#             search_fields = ['title','body']
#             filter_backends = [DjangoFilterBackend, SearchFilter]
#             queryset = CreateBlog.objects.all()
#             serializer = CreateBlogSerializer(queryset, many=True)
#             return Response(serializer.data)
#         except CreateBlog.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)


class SearchView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    search_fields = ['title','body','user_id_id__username']
    filter_backends = (filters.SearchFilter,)
    queryset = CreateBlog.objects.all()
    serializer_class = CreateBlogSerializer




@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteBlog(request,blog_id):
    try:
        CreateBlog.objects.filter(user_id_id=request.user.id).get(blog_id = blog_id).delete()
        return Response(status=status.HTTP_201_CREATED)
    except CreateBlog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateBlog(request,pk):
    try:
        shipment = CreateBlog.objects.get(pk=pk)
    except CreateBlog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CreateBlogSerializer(shipment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userBlog(request):
    try:
        shipment = CreateBlog.objects.filter(user_id_id=request.user.id)
        serializer = CreateBlogSerializer(shipment, many=True)
        return Response(serializer.data)
    except:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def savedBlog(request):
    try:
        shipment = CreateBlog.objects.exclude(user_id_id=request.user.id).filter(likes = request.user.id)
        serializer = CreateBlogSerializer(shipment, many=True)
        return Response(serializer.data)
    except:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def otherUserBlog(request):
    try:
        shipment = CreateBlog.objects.exclude(user_id_id = request.user.id)
        serializer = CreateBlogSerializer(shipment, many=True)
        return Response(serializer.data)
    except:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBlog(request,pk):
    try:
        shipment = CreateBlog.objects.get(pk=pk)
    except CreateBlog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CreateBlogSerializer(shipment)
        return Response(serializer.data)

@api_view(['POST'])
def deletetokens(request):
    try:
        AuthToken.objects.all().delete()
        return Response(status=status.HTTP_201_CREATED)
    except AuthToken.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


