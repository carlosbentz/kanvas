from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from accounts.permissions import IsInstructor
from .serializers import CourseSerializer
from .models import Course
from django.shortcuts import get_object_or_404


class CourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructor]
    
    def get(self, request):
        courses = Course.objects.all()
        courses = CourseSerializer(courses, many=True)
        
        return Response(courses.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        course = CourseSerializer(data=data)

        if not course.is_valid():
            return Response(course.errors, status=status.HTTP_400_BAD_REQUEST)

        course = Course.objects.get_or_create(**course.validated_data)[0]

        course = CourseSerializer(course)

        return Response(course.data, status=status.HTTP_201_CREATED)


class RetrieveCourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructor]
    
    def get(self, request, course_id):
        try:
            course =  Course.objects.get(id=course_id)

        except Course.DoesNotExist:
            return Response(
                {"errors": "invalid course_id"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        course = CourseSerializer(course)

        return Response(course.data, status=status.HTTP_200_OK)


    def delete(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        
        course.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseEnrollView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructor]

    def put(self, request, course_id):
        try:
            course =  Course.objects.get(id=course_id)

        except Course.DoesNotExist:
            return Response(
                {"errors": "invalid course_id"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            user_ids = request.data["user_ids"]
        except TypeError:
            return Response(
                {"error": "User id list were not provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        except KeyError:
            return Response(
                {"error": "User id list were not provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if type(user_ids) is not list:
            return Response({"error":"user_ids must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = []
        for id in user_ids:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return Response(
                    {"errors": "invalid user_id list"},
                    status=status.HTTP_404_NOT_FOUND
                )

        for id in user_ids:
            try:
                queryset.append(User.objects.get(id=id, is_staff=False, is_superuser=False))
            except User.DoesNotExist:
                return Response(
                    {"errors": "Only students can be enrolled in the course."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        course.users.set(queryset)
        course = CourseSerializer(course)

        return Response(course.data, status=status.HTTP_200_OK)


    def delete(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        course.users.clear()

        return Response(status=status.HTTP_204_NO_CONTENT)
