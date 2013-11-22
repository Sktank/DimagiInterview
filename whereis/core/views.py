# Create your views here.
from django.core import serializers
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import datetime
from core.models import Location, Employee
import urllib2
import ast
import re



def base(request, template="core/base.html"):
    employees = Employee.objects.all()
    employee_names = []
    for employee in employees:
        employee_names.append(employee.firstName + ' ' + employee.lastName)
    vals = dict(employee_names=employee_names)
    return render_to_response(template, vals)

@csrf_exempt
def save(request):
    if request.is_ajax():
        success_message = "saved!"
        invalid_name_message = "the name you entered is invalid"
        address = request.POST.get('address', False)
        lng = request.POST.get('longitude', False)
        lat = request.POST.get('latitude', False)
        name = request.POST.get('name', False).strip()
        if not re.search('^\w* \w*$', name):
            return HttpResponse(invalid_name_message)
        firstName = name.split(' ')[0]
        lastName = name.split(' ')[1]

        employee = Employee.objects.filter(firstName=firstName, lastName=lastName)
        if not employee:
            employee = Employee(firstName=firstName, lastName=lastName, numLocations=0)
            employee.save()
        else:
            employee = employee[0]

        location = Location(lat=lat, lng=lng, address=address, employee=employee, time=datetime.datetime.utcnow())
        location.save()
        employee.numLocations += 1
        employee.save()
        return HttpResponse(success_message)

@csrf_exempt
def getLocations(request):
    if request.is_ajax():
        name = request.POST.get('name', False)
        firstName = name.split(' ')[0]
        lastName = name.split(' ')[1]
        locations = Location.objects.filter(employee__firstName=firstName, employee__lastName=lastName)
        data = serializers.serialize("json", locations)
        return HttpResponse(data)
