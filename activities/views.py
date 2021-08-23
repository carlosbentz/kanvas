from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from accounts.permissions import IsInstructor, IsFacilitator, IsStudent
from .serializers import ActivitySerializer, SubmissionSerializer, RateSubmissionSerializer
from .models import Activity, Submission
from django.shortcuts import get_object_or_404


class ActivityView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructor | IsFacilitator]
    
    def get(self, request):
        user = request.user

        if not user.is_staff and not user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)

        activities = Activity.objects.all()
        activities = ActivitySerializer(activities, many=True)
        
        return Response(activities.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        activity = ActivitySerializer(data=data)

        if not activity.is_valid():
            return Response(activity.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            activity = Activity.objects.get_or_create(**activity.validated_data)[0]

        except IntegrityError:
            points = activity.validated_data["points"]
            activity = Activity.objects.get(title=activity.validated_data["title"])
            activity.points = points
            activity.save()

        activity = ActivitySerializer(activity)

        return Response(activity.data, status=status.HTTP_201_CREATED)


class CreateSubmissionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStudent]
    

    def post(self, request, activity_id=None):
        data = request.data
        data["activity_id"] = activity_id
        data["user_id"] = request.user.id

        submission = SubmissionSerializer(data=data)

        if not submission.is_valid():
            return Response(submission.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            submission = Submission.objects.create(**submission.validated_data)

        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        submission = SubmissionSerializer(submission)

        return Response(submission.data, status=status.HTTP_201_CREATED)


class RateSubmissionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsFacilitator | IsInstructor]
    

    def put(self, request, submission_id=None):
        data = request.data

        submission = RateSubmissionSerializer(data=data)

        if not submission.is_valid():
            return Response(submission.errors, status=status.HTTP_400_BAD_REQUEST)

        submission = get_object_or_404(Submission, id=submission_id)
        
        if data["grade"] > submission.activity.points or data["grade"] < 0:
            return Response({"error": "Invalid grade"}, status=status.HTTP_400_BAD_REQUEST)

        submission.grade = data["grade"]
        submission.save()

        submission = SubmissionSerializer(submission)

        return Response(submission.data, status=status.HTTP_200_OK)


class GetSubmissionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

    def get(self, request):
        user = request.user
        if not user.is_staff and not user.is_superuser:
            submissions = Submission.objects.filter(user_id=user.id)

        else:
            submissions = Submission.objects.all()

        submissions = SubmissionSerializer(submissions, many=True)
        
        return Response(submissions.data, status=status.HTTP_200_OK)
