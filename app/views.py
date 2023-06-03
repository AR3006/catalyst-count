from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import csv
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
import json

@csrf_exempt
def login(request):
    return render(request, "login.html")

@csrf_exempt
def render_upload_file_page(request):
    return render(request, "upload_file.html")

@csrf_exempt
def render_query_builder_page(request):
    return render(request, "query_builder.html")

@csrf_exempt
def on_login(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    if username and password:
        return redirect(render_upload_file_page)


progress_value = 0

def get_progress(request):
    # this function is use to get data to update progressbar for data file upload
    global progress_value
    return HttpResponse(json.dumps(progress_value), content_type='application/json')

import time
@csrf_exempt
@api_view(['POST'])
def on_upload_file(request):
    global progress_value
    from django.utils import timezone
    start_time = timezone.now()
    handle_uploaded_file(request.FILES["file"])
    with open('name.txt', "r",  encoding="utf-8" ,errors='ignore',) as csv_file:
        data = csv.reader(csv_file, delimiter=",")
        next(data)
        result_list = []
        for row in data:
            result_dict = CSVData(
                keyword_number = str(row[0]),
                name = str(row[1]),
                domain = str(row[2]),
                year_founded = str(row[3]),
                industry = str(row[4]),
                size_range = str(row[5]),
                locality = str(row[6]),
                country = str(row[7]),
                linkedin_url = str(row[8]),
                current_employee_estimate = str(row[9]),
                total_employee_estimate = str(row[10]),
            )
            
            result_list.append(result_dict)
            if len(result_list)>7173:
                progress_value+=0.1
                CSVData.objects.bulk_create(result_list)
                result_list = []
        
        if result_list:
                progress_value+=0.1
                CSVData.objects.bulk_create(result_list)
    
    end_time = timezone.now()
    print("TOTAL SECOND >>>> ",(end_time-start_time).total_seconds())
    time.sleep(2)
    progress_value = 0
    return redirect(render_upload_file_page)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def on_filter(request):
    data_dict = {
        "keyword_number":request.GET.get('keyword_number',None),
        "name":request.GET.get('name',None),
        "domain":request.GET.get('domain',None),
        "year_founded":request.GET.get('year_founded',None),
        "industry":request.GET.get('industry',None),
        "size_range":request.GET.get('size_range',None),
        "locality":request.GET.get('locality',None),
        "country":request.GET.get('country',None),
        "linkedin_url":request.GET.get('linkedin_url',None),
        "current_employee_estimate":request.GET.get('current_employee_estimate',None),
        "total_employee_estimate":request.GET.get('total_employee_estimate',None),
    }
    params = {}
    for key, value in data_dict.items():
        if value!=None:
            params[key] = value
    
    return render(request,"query_result.html")


def handle_uploaded_file(f):
    global progress_value
    with open("name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def filter_model(params):
    data = list(CSVData.objects.filter(**params).values())
    return data 