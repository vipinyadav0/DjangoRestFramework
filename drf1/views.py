
from urllib import response

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from rest_framework import generics, mixins, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from drf1 import serializers

from .forms import StudentForm
from .models import Student
from .permissions import IsAuthorOrReadOnly
from .serializers import StudentModelSerializer, StudentSerializer

# Api ViewSet
class StudentsViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    model = Student
    queryset = Student.objects.all()
    serializer_class =  StudentModelSerializer


# Function Based Views

def students(request):
    stu = Student.objects.all()
    serializer = StudentSerializer(stu, many=True)
    json_data = JSONRenderer().render(serializer.data)
    # return HttpResponse(json_data, content_type ='application/json' )
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def model_student(request):
    """list of all the students and we can update on particular student data

    Args:
        request (_type_): _description_
    """
    if request.method =="GET":
        snippets = Student.objects.all()
        serializer = StudentModelSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method=="POST":
        data = JSONParser().parse(request)
        serializer = StudentModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def student_detail(request, pk):
    """Retrieve, delete, update a code snippet

    Args:
        request (_type_): _description_
    """
    try:
        snippet = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return HttpResponse(status = 404)
    if request.method=="GET":
        serializer = StudentModelSerializer(snippet)
        return JsonResponse(serializer.data)
    elif request.method=="PUT":
        data = JSONParser().parse(request)
        serializer = StudentModelSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method=="DELETE":
        snippet.delete()
        return HttpResponse(status=204)


# Class based views

class StudentList(APIView):
    """List of all students or create a new student

    Args:
        APIView (_type_): _description_
    """
    def get(self, request, format=None):
        snippet = Student.objects.all()
        serializer = StudentModelSerializer(snippet, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StudentDetail(APIView):
    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        snippet = Student.objects.get(pk=pk)
        serializer = StudentModelSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = Student.objects.get(pk=pk)
        serializer = StudentModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#using mixin

'''
One of the big wins of using class-based views is that it allows us to easily compose reusable bits of behaviour.

The create/retrieve/update/delete operations that we've been using so far are going to be pretty similar for any model-backed API views we create. Those bits of common behaviour are implemented in REST framework's mixin classes.

'''
class StudentMixinList(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class StudentCrud(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer = StudentModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
# using generic class based views

class StudentGenericList(generics.ListCreateAPIView):
    # permission_classes = (permissions.IsAuthenticated,) # adding...is authenticated to use API if user is logged in and also called View Level Permission 
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

class SetudentGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly, )
    # permission_classes = (permissions.IsAuthenticated,) # adding...is authenticated to use API if user is logged in and also called View Level Permission 
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

# class to create data via CreateAPIView imported from generics
class StudentCreateView(CreateAPIView):
    serializer_class = StudentModelSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

# class to delete data via DestroyAPIView imported from generics
class StudentDestroy(DestroyAPIView):
    queryset = Student.objects.all()
    lookup_field = 'id'

    # overriding the destroy function
    def delete(self, request, *args, **kwargs):
        student_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('student_data_{}'.format(student_id))
        return response

#using RetrieveUpdateDestroyView for performing Retriving a data, updating a data, deleting a data
class StudentRetriveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    lookup_field = 'id'
    serializer_class = StudentModelSerializer

    # overriding the destroy function
    def delete(self, request, *args, **kwargs):
        student_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('student_data_{}'.format(student_id))
        return response

    def update(self ,request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code==200:
            from django.core.cache import cache
            student = response.data
            cache.set('product_data_{}'.format(student['id']), {
                'name':student['name'],
                'roll_no':student['roll_no'],
                'city': student['city'],
            })
        return response

# Creating Student Via form and sending mail
class CreateStudent(CreateView):
    template_name = "drf1/home.html",
    form_class = StudentForm

    def get_success_url(self):
        return 'drf1/home.html'


