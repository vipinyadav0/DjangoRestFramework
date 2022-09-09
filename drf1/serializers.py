from dataclasses import field
from statistics import mode
from rest_framework import serializers
from .models import Student


# class StudentSerializer(serializers.serializerserializer):
#     class Meta:
#         model = Student
#         fields = '__all__'

class StudentSerializer(serializers.Serializer):
    created = serializers.DateTimeField()
    name = serializers.CharField(max_length=100, allow_blank=True, allow_null=True)
    roll_no = serializers.IntegerField()
    city = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.title)
        instance.roll_no = validated_data.get('roll_no', instance.code)
        instance.city = validated_data.get('city', instance.linenos)
        instance.save()
        return instance

class StudentModelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.name')
    class Meta:
        model = Student
        fields = '__all__'
