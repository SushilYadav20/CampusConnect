from django.shortcuts import render
from .serializer import *
from .models import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import authentication_classes,permission_classes 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout,login
from datetime import date

# Create your views here.

class SignupView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self,request):
        user=CustomUser.objects.all()
        serializer_data=SignupSerializer(user,many=True).data
        return Response({'message':'User data get Successfully','data':serializer_data},status=status.HTTP_200_OK)
    
    def post(self,request):

        data=request.data.copy()
        if data.get('role').lower()=='admin':
            data['is_staff']=True
        serializer_data = SignupSerializer(data=data)
        if serializer_data.is_valid():
            user=serializer_data.save()
            user.set_password(request.data.get('password'))
            user.save()
            return Response({'message':'User Created Successfully','data':serializer_data.data},status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request):
        data=request.data
        id= data.get('id')
        
        if request.user.role != 'admin':
            return Response({'message':'Only allowed for admin'},status=status.HTTP_401_UNAUTHORIZED)
        if not CustomUser.objects.filter(id=id).exists():
           return Response({'message':'id does not exist'},status=status.HTTP_404_NOT_FOUND)
        else:
            id=CustomUser.objects.get(id=id)
            serializer_data = SignupSerializer(id,data=data,partial=True)
            if serializer_data.is_valid():
                user=serializer_data.save()
                user.set_password(request.data.get('password'))
                user.save()
                return Response({'message':'Student Profile Updated Successfully','data':serializer_data.data},status=status.HTTP_200_OK)
            return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self,request):
        data=request.data
        username=data.get('username')
        password=data.get('password')
        user=authenticate(username=username,password=password)
        token,created=Token.objects.get_or_create(user=user)
        if user:
            return Response({'message':'User logged in successfully','token':token.key},status=status.HTTP_200_OK)
        else:
            return Response({'message':'Invalid Credentials'},status=status.HTTP_400_BAD_REQUEST)
        

class LogoutView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        data=request.user
        # if data.is_authenticated:
        #     logout(request)
        data.auth_token.delete()
        return Response({"message": "Logged out successfully."})


#### CRUD FOR STUDENT PROFILE ###

class StudentProfileView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        user=StudentProfile.objects.all()
        serializer_data=StudentProfileSerializer(user,many=True).data
        return Response({'message':'Student data get Successfully','data':serializer_data},status=status.HTTP_200_OK)
    
    def post(self,request):
        if request.user.role != 'admin':
            return Response({'message':'You do not have permission to perform this action'},status=status.HTTP_401_UNAUTHORIZED)
        data=request.data
        serializer_data = StudentProfileSerializer(data=data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response({'message':'Student Profile Created Successfully','data':serializer_data.data},status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
        

    def patch(self,request):
        data=request.data
        student_id= data.get('student_id')
        
        if request.user.role != 'admin':
            return Response({'message':'Only allowed for admin'},status=status.HTTP_401_UNAUTHORIZED)
        if not StudentProfile.objects.filter(id=student_id).exists():
           return Response({'message':'id does not exist'},status=status.HTTP_404_NOT_FOUND)
        else:
            student_id=StudentProfile.objects.get(id=student_id)
            serializer_data = StudentProfileSerializer(student_id,data=data,partial=True)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response({'message':'Student Profile Updated Successfully','data':serializer_data.data},status=status.HTTP_200_OK)
            return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
 
    def delete(self,request):
        data=request.data
        student_id=data.get('student_id')
        if not request.user.role == 'admin':
            return Response({'message':'Only allowed for admin'},status=status.HTTP_401_UNAUTHORIZED)
        if not StudentProfile.objects.filter(id=student_id).exists():
            return Response({'message':'student id does not exists','response_code':400})
        StudentProfile.objects.get(id=student_id).delete()
        return Response({'message':'student deleted successfully','response_code':200})
    

#### CRUD FOR FACULTY ###

class FacultyView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user=Faculty.objects.all()
        serializer_data=FacultySerializer(user,many=True).data
        return Response({'message':'Faculty data get Successfully','data':serializer_data},status=status.HTTP_200_OK)
    
    
    def post(self,request):
        if request.user.role != 'admin':
            return Response({'message':'You do not have permission to perform this action'},status=status.HTTP_401_UNAUTHORIZED)
        data=request.data
        faculty=data.get('faculty')
        if  Faculty.objects.filter(faculty_id=faculty).exists():
            return Response({'message':' Already profile created'},status=status.HTTP_404_NOT_FOUND)

        serializer_data = FacultySerializer(data=data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response({'message':'Faculty Created Successfully','data':serializer_data.data},status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request):

        data=request.data
        faculty_id= data.get('faculty_id')
        
        if not request.user.role == 'admin':
            return Response({'message':'Only allowed for admin'},status=status.HTTP_401_UNAUTHORIZED)
        if not CustomUser.objects.filter(id=faculty_id):
           return Response({'message':'id does not exist'},status=status.HTTP_404_NOT_FOUND)
        else:
            faculty_id=Faculty.objects.get(id=faculty_id)
            serializer_data = FacultySerializer(faculty_id,data=data,partial=True)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response({'message':' Faculty Updated Successfully','data':serializer_data.data},status=status.HTTP_200_OK)
            return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
  
    def delete(self,request):
        data=request.data
        faculty_id=data.get('faculty_id')
        if request.user.role != 'admin':
            return Response({'message':'You do not have permission to perform this action'},status=status.HTTP_401_UNAUTHORIZED)
        if not Faculty.objects.filter(id=faculty_id).exists():
            return Response({'message':'faculty id does not exists','response_code':400})
        Faculty.objects.get(id=faculty_id).delete()
        return Response({'message':'faculty deleted successfully','response_code':200})
    

#### CRUD FOR DEPARTMENT ###



class DepartmentView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]

    def get(self,request):
        user=Department.objects.all()
        serializer_data=DepartmentSerializer(user,many=True).data
        return Response({'message':'Department data get Successfully','data':serializer_data},status=status.HTTP_200_OK)
    
    def post(self,request):
        data=request.data
        department_name=data.get('department_name')
        if Department.objects.filter(department_name=department_name).exists():
            return Response({'message':'Department already exists'},status=status.HTTP_400_BAD_REQUEST)
        serializer_data = DepartmentSerializer(data=data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response({'message':'Department Created Successfully','data':serializer_data.data},status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request):
        data=request.data
        department_id= data.get('department_id')
        # if not request.user.role == 'admin':
        #     return Response({'message':'Only allowed for admin'},status=status.HTTP_401_UNAUTHORIZED)
        if not Department.objects.filter(id=department_id).exists():
           return Response({'message':'id does not exist'},status=status.HTTP_404_NOT_FOUND)
        else:
            department_id=Department.objects.get(id=department_id)
            serializer_data = DepartmentSerializer(department_id,data=data,partial=True)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response({'message':'Department Updated Successfully','data':serializer_data.data},status=status.HTTP_200_OK)
            return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self,request):
        data=request.data
        department_id=data.get('department_id')
        if not Department.objects.filter(id=department_id).exists():
            return Response({'message':' id does not exists','response_code':400})
        Department.objects.get(id=department_id).delete()
        return Response({'message':'Department deleted successfully','response_code':200})


#### CRUD FOR SUBJECT ###



class SubjectListView(APIView):

    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]

    def get(self,request):
        user=SubjectList.objects.all()
        serializer_data=SubjectListSerializer(user,many=True).data
        return Response({'message':'Subject get Successfully','data':serializer_data},status=status.HTTP_200_OK)
    
    def post(self,request):
        data=request.data
        subject_name=data.get('subject_name')
        if SubjectList.objects.filter(subject_name=subject_name).exists():
            return Response({'message':'Subject already exists'},status=status.HTTP_400_BAD_REQUEST)
        serializer_data = SubjectListSerializer(data=data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response({'message':'Subject Created Successfully','data':serializer_data.data},status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request):
        data=request.data
        subject_id= data.get('subject_id')
        # if not request.user.role == 'admin':
        #     return Response({'message':'Only allowed for admin'},status=status.HTTP_401_UNAUTHORIZED)
        if not SubjectList.objects.filter(id=subject_id).exists():
           return Response({'message':'id does not exist'},status=status.HTTP_404_NOT_FOUND)
        else:
            subject_id=SubjectList.objects.get(id=subject_id)
            serializer_data = SubjectListSerializer(subject_id,data=data,partial=True)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response({'message':'Subject Updated Successfully','data':serializer_data.data},status=status.HTTP_200_OK)
            return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self,request):
        data=request.data
        subject_id=data.get('subject_id')
        if not SubjectList.objects.filter(id=subject_id).exists():
            return Response({'message':' id does not exists','response_code':400})
        SubjectList.objects.get(id=subject_id).delete()
        return Response({'message':'Subject deleted successfully','response_code':200})
    

#### CRUD FOR SEMESTER ###

class SemesterView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]

    def get(self,request):
        user=Semester.objects.all()
        serializer_data=SemesterSerializer(user,many=True).data
        return Response({'message':'Semester get Successfully','data':serializer_data},status=status.HTTP_200_OK)
    
    def post(self,request):
        data=request.data
        serializer_data = SemesterSerializer(data=data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response({'message':'Semester Created Successfully','data':serializer_data.data},status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request):
        data=request.data
        semester_id= data.get('semester_id')
       
        if not Semester.objects.filter(id=semester_id).exists():
           return Response({'message':'id does not exist'},status=status.HTTP_404_NOT_FOUND)
        else:
            semester_id=Semester.objects.get(id=semester_id)
            serializer_data = SemesterSerializer(semester_id,data=data,partial=True)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response({'message':'Semester Updated Successfully','data':serializer_data.data},status=status.HTTP_200_OK)
            return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self,request):
        data=request.data
        semester_id=data.get('semester_id')
        if not Semester.objects.filter(id=semester_id).exists():
            return Response({'message':' id does not exists','response_code':400})
        Semester.objects.get(id=semester_id).delete()
        return Response({'message':'Semester deleted successfully','response_code':200})
    

#### CRUD FOR Assignment ###

class AssignmentView(APIView):

    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        user=Assignment.objects.all()
        serializer_data=AssignmentSerializer(user,many=True).data
        return Response({'message':'Assignment get Successfully','data':serializer_data},status=status.HTTP_200_OK)
    
    def post(self,request):
        data=request.data
        if request.user.role != 'faculty':
            return Response({'message':'You do not have permission to perform this action'},status=status.HTTP_401_UNAUTHORIZED)
        serializer_data = AssignmentSerializer(data=data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response({'message':'Assignment Created Successfully','data':serializer_data.data},status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request):
        data=request.data
        Assignment_id= data.get('Assignment_id')
        if request.user.role != 'faculty':
            return Response({'message':'You do not have permission to perform this action'},status=status.HTTP_401_UNAUTHORIZED)
        if not Assignment.objects.filter(id=Assignment_id).exists():
           return Response({'message':'id does not exist'},status=status.HTTP_404_NOT_FOUND)
        else:
            Assignment_id=Assignment.objects.get(id=Assignment_id)
            serializer_data = AssignmentSerializer(Assignment_id,data=data,partial=True)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response({'message':'Assignment Updated Successfully','data':serializer_data.data},status=status.HTTP_200_OK)
            return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self,request):
        data=request.data
        Assignment_id=data.get('Assignment_id')
        if request.user.role != 'faculty':
            return Response({'message':'You do not have permission to perform this action'},status=status.HTTP_401_UNAUTHORIZED)
        if not Assignment.objects.filter(id=Assignment_id).exists():
            return Response({'message':' id does not exists','response_code':400})
        Assignment.objects.get(id=Assignment_id).delete()
        return Response({'message':'Assignment deleted successfully','response_code':200})
    
#### CRUD FOR AssignmentSubmission ###


class AssignmentSubmissionView(APIView):

    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user=AssignmentSubmission.objects.all()
        serializer_data=AssignmentSubmissionSerializer(user,many=True).data
        return Response({'message':'AssignmentSubmission get Successfully','data':serializer_data},status=status.HTTP_200_OK)
    
    def post(self,request):
        data=request.data
        if request.user.role != 'student':
            return Response({'message':'You do not have permission to perform this action'},status=status.HTTP_401_UNAUTHORIZED)
        serializer_data = AssignmentSubmissionSerializer(data=data)

        if serializer_data.is_valid():
            serializer_data.save()
            return Response({'message':'Assignment Submitted Successfully','data':serializer_data.data},status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request):
        data=request.data
        submission_id= data.get('submission_id')
        if request.user.role != 'faculty':
            return Response({'message':'You do not have permission to perform this action'},status=status.HTTP_401_UNAUTHORIZED)
        if not AssignmentSubmission.objects.filter(id=submission_id).exists():
           return Response({'message':'id does not exist'},status=status.HTTP_404_NOT_FOUND)
        else:
            submission=AssignmentSubmission.objects.get(id=submission_id)
            serializer_data = AssignmentSubmissionSerializer(submission,data=data,partial=True)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response({'message':'AssignmentSubmission Updated Successfully','data':serializer_data.data},status=status.HTTP_200_OK)
            return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self,request):
        data=request.data
        submission_id=data.get('submission_id')
        if request.user.role != 'faculty':
            return Response({'message':'You do not have permission to perform this action'},status=status.HTTP_401_UNAUTHORIZED)
        if not AssignmentSubmission.objects.filter(id=submission_id).exists():
            return Response({'message':' id does not exists','response_code':400})
        AssignmentSubmission.objects.get(id=submission_id).delete()
        return Response({'message':'AssignmentSubmission deleted successfully','response_code':200})


#### CRUD FOR Attendance ###

class AttendanceView(APIView):

    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        user=Attendance.objects.all()
        serializer_data=AttendanceSerializer(user,many=True).data
        return Response({'message':'Attendance get Successfully','data':serializer_data},status=status.HTTP_200_OK)
    
    def post(self,request):
        data=request.data
        today=date.today()
        student=data.get('student')
        subject=data.get('subject')
        
        if request.user.role != 'faculty':
            return Response({'message':'You do not have permission to perform this action'},status=status.HTTP_401_UNAUTHORIZED)
        if not StudentProfile.objects.filter(id=student).exists():
            return Response({'message':'Student id does not exists'},status=status.HTTP_404_NOT_FOUND)
    
        if Attendance.objects.filter(student=student,date=today,subject=subject).exists():
            return Response({'message':'You have already marked your attendance'},status=status.HTTP_400_BAD_REQUEST)
            
        serializer_data = AttendanceSerializer(data=data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response({'message':'Attendance registed successfully','data':serializer_data.data},status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
    
class AttendanceListView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]

    def get (self,request):
        attendance=Attendance.objects.all()
        serializer_data=AttendanceSerializer(attendance,many=True).data
        return Response({'message':'Attendance get Successfully','data':serializer_data},status=status.HTTP_200_OK)
    

class UploadResourceView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get (self,request):
        resources=Resources.objects.all()
        serializer_data=ResourcesSerializer(resources,many=True).data
        return Response({'message':'Resources get Successfully','data':serializer_data},status=status.HTTP_200_OK)
    
    def post(self, request):
        data=request.data
        uploaded_by=data.get('uploaded_by')

        if request.user.role != 'faculty':
            return Response({'message': 'Only faculty can upload resources'}, status=status.HTTP_403_FORBIDDEN)
        if not Faculty.objects.filter(id=uploaded_by).exists():
            return Response({'message':'Faculty id does not exists'},status=status.HTTP_404_NOT_FOUND)
      
        serializer = ResourcesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Resource uploaded successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        data=request.data
        resource_id=data.get('resource_id')

        if request.user.role != 'faculty':
            return Response({'message': 'Only faculty can upload resources'}, status=status.HTTP_403_FORBIDDEN)
        if not Resources.objects.filter(id=resource_id).exists():
            return Response({'message':'Resource id does not exists'},status=status.HTTP_404_NOT_FOUND)

        id=Resources.objects.get(id=resource_id)      
        serializer = ResourcesSerializer(id,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Resource updated successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        resource_id=request.data.get('resource_id')
        if request.user.role != 'faculty':
            return Response({'message': 'Only faculty can upload resources'}, status=status.HTTP_403_FORBIDDEN)
        if not Resources.objects.filter(id=resource_id).exists():
            return Response({'message':'Resource id does not exists'},status=status.HTTP_404_NOT_FOUND)
        Resources.objects.get(id=resource_id).delete()
        return Response({'message':'Resource deleted successfully'},status=status.HTTP_200_OK)

