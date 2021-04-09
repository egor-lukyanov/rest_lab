from rest_framework import serializers

from main import models


class JobSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        fields = '__all__'
        read_only_fields = ('status', 'result')
        model = models.Job


class JobResultSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = models.JobResult
