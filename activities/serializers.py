from rest_framework import serializers
from accounts.serializers import UserSerializer


class SubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    repo = serializers.CharField()
    grade = serializers.IntegerField(read_only=True)
    activity_id = serializers.IntegerField()
    user_id = serializers.IntegerField()


class ActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    points = serializers.IntegerField()
    submissions = SubmissionSerializer(many=True, read_only=True)


class RateSubmissionSerializer(serializers.Serializer):
    grade = serializers.IntegerField()
