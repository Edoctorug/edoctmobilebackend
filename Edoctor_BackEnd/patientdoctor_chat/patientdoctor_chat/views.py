from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import sessions
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from chatapp.models import HospitalUsers
from chatapp.models import Patients
from chatapp.models import Doctors


# Create your views here.


def mainEntry(request):
	json_response_mdl = {
	"status_code": 200,
    "message":"welccome"
	}

	response_mdl = json.dumps(json_response_mdl)
	return HttpResponse(response_mdl)