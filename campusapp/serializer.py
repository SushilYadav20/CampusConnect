from rest_framework import serializers
from .models import *

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','password','email','first_name','last_name','role','is_staff'] 


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class SubjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectList
        fields = '__all__'       

class StudentProfileSerializer(serializers.ModelSerializer):
    first_name=serializers.ReadOnlyField(source='student.first_name')
    last_name=serializers.ReadOnlyField(source='student.last_name')
    class Meta:
        model = StudentProfile
        fields = '__all__' 

class FacultySerializer(serializers.ModelSerializer):
    first_name=serializers.ReadOnlyField(source='faculty.first_name')
    last_name=serializers.ReadOnlyField(source='faculty.last_name')

    class Meta:
        model = Faculty
        fields = '__all__' 

class SemesterSerializer(serializers.ModelSerializer):
    subject_name=serializers.ReadOnlyField(source='subject.subject_name')
    subject_code=serializers.ReadOnlyField(source='subject.subject_code')

    class Meta:
        model = Semester
        fields = '__all__' 


class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = '__all__' 


class AssignmentSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignmentSubmission
        fields = '__all__' 

class AttendanceSerializer(serializers.ModelSerializer):
    student_f=serializers.ReadOnlyField(source='student.student.first_name')
    student_l=serializers.ReadOnlyField(source='student.student.last_name')

    class Meta:
        model = Attendance
        fields = '__all__' 

class ResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resources
        fields = '__all__'
        