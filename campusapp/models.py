from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin','Admin'),
        ('faculty','Faculty'),
        ('student','Student'),
    ] 
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='admin')
    
class Department(models.Model):
   department_name = models.CharField(max_length=30)
   
class SubjectList(models.Model):
    department_name=models.ForeignKey(Department,on_delete=models.CASCADE,related_name='dept_name')
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=30,unique=True)

class Semester(models.Model):
    semester=models.CharField(max_length=20)
    subject=models.ForeignKey(SubjectList,on_delete=models.CASCADE,related_name='subject')
    department_name=models.ForeignKey(Department,on_delete=models.CASCADE,related_name='dep_name')


class StudentProfile(models.Model):
    student=models.ForeignKey(CustomUser,on_delete=models.CASCADE,limit_choices_to={'role':'student'},related_name='student')
    enrollment_number=models.PositiveIntegerField(unique=True)
    department=models.ForeignKey(Department,on_delete=models.CASCADE,related_name='department')
    batch = models.CharField(max_length=20)
    mobile = models.BigIntegerField()

class Faculty(models.Model):
    faculty=models.ForeignKey(CustomUser,on_delete=models.CASCADE,limit_choices_to={'role':'faculty'},related_name='faculty')
    employee_id=models.CharField(max_length=20,unique=True)
    department=models.ForeignKey(Department,on_delete=models.CASCADE,related_name='faculty_department')
    designation = models.CharField(max_length=30)


class Assignment(models.Model):
    title= models.CharField(max_length=100)
    description=models.TextField(blank=True)
    due_date=models.DateField()
    assignment_file=models.FileField(upload_to='assignment/')
    created_by=models.ForeignKey(Faculty,on_delete=models.CASCADE)
    subject=models.ForeignKey(SubjectList,on_delete=models.CASCADE)

class AssignmentSubmission(models.Model):
    Status = [
        ('submitted','Submitted'),
        ('reviewed','Reviewed'),
        ('rejected','Rejected'),
    ]

    assignment=models.ForeignKey(Assignment,on_delete=models.CASCADE)
    student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
    submitted_assignment=models.FileField(upload_to='submitted_assignment/')
    status=models.CharField(max_length=20,choices=Status)
    feedback=models.CharField(max_length=50,null=True,blank=True)

class Attendance(models.Model):
    Status = [
        ('present','Present'),
        ('absent','Absent'),
    ]
    student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    subject=models.ForeignKey(SubjectList,on_delete=models.CASCADE)
    status=models.CharField(max_length=20,choices=Status)

class Resources(models.Model):
    title=models.CharField(max_length=50)
    description = models.TextField(blank=True)
    subject=models.ForeignKey(SubjectList,on_delete=models.CASCADE)
    resource_file=models.FileField(upload_to='resources/')
    uploaded_by=models.ForeignKey(Faculty,on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    