from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import sessions
from django.views.decorators.csrf import csrf_exempt
import json, os
from django.http import FileResponse
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from chatapp.models import HospitalUsers
from chatapp.models import Patients
from chatapp.models import Doctors
from patientdoctor_chat.settings import BASE_DIR

from .ResponseModel import ResponseMdl
# Create your views here.
specialities = ["consultant","Dentist","Physician","Dermatologist","Surgeon","Counselor","Psychiatrist","Pediatricians","Obstetrician","Nurse","Orthopedologist","Optician","Therapist","Pharmacist","Midwife","Nutritionist","Gynecologist","Urologist"]

def authUser(json_post):#function to authenticate the user
     """
     Authenticates the user based on the provided JSON data.

     Args:
        json_post (dict): JSON data containing user credentials.

     Returns:
        AuthenticationResult: The result of the authentication process.
     """
     user_name = json_post["user_name"]#get username
     user_pwd = json_post["user_password"]#password in auth request 
     print("\tauthenticating: ",user_name," : ",user_pwd)
     auth_res = authenticate(username=user_name,password=user_pwd) #authenticate the user in the auth_user database using the username and password 

     if auth_res == None: #check if user is authencated
          return [None,None] #return None if user credentials are false
     print("fly or die")
     auth_uid  = auth_res.pk #get current user id as primary key

     #first_name = auth_res["first_name"]
     #last_name = auth_res["last_name"]

     user_names = auth_res.get_full_name()#get current user full names 
    
     print(f"using auth id: {auth_uid} with name {user_names}")
     active_user = HospitalUsers.objects.get(user_id=auth_uid)
     #HospitalUsers.objects.filter(user_id=auth_uid).values()[0]["user_role"] #get current user type basing on the user_id
     active_user_role = active_user.user_role
     active_role_group = active_user.role_group
     user_data = [auth_uid,{
          "names": user_names,
          "user_role": active_user_role,
          "role_group":active_role_group,
          "extra_data": ["consultant","Dentist","Physician","Dermatologist","Surgeon","Counselor","Psychiatrist","Pediatricians","Obstetrician","Nurse","Orthopedologist","Optician","Therapist","Pharmacist","Midwife","Nutritionist","Gynecologist","Urologist"]
     }] #an array having user id and user information object 
     
     print(user_data)
     
     return user_data #return user information 


@csrf_exempt
def auth_user(request): #user authentication view
    """
    Handles user authentication view.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The HTTP response.
    """
    print("new request")
    #print(request)
    json_post_str = request.body #get raw request data
    json_post = json.loads(json_post_str) #turn raw data to json object
    print(json_post)

    auth_uid,auth_status = authUser(json_post)#call user authentication function

    if auth_status != None:
         request.session["auth_man"] = auth_uid

         print("\n\nauth man is: ", request.session["auth_man"])
         response_mdl = ResponseMdl(200,"Welcome",auth_status)
         return HttpResponse(response_mdl.serial())
    response_mdl = ResponseMdl(500,"User Error")
    return HttpResponse(response_mdl.serial())

def createDoctor(json_post):#add Doctor to the database entry
    """
    Adds a new doctor to the database based on the provided JSON data.

    Args:
        json_post (dict): JSON data containing doctor details.

    Returns:
        Doctor object as dictionary
    """
    user_name = json_post["user_name"]#doctors username
    temp_int_user_role = int(json_post["user_role"])
    int_user_role = 0 if (temp_int_user_role >= len(specialities)) else temp_int_user_role
    user_role = specialities[int_user_role]
    user_password = json_post["user_password"]
    user_first_name = json_post["first_name"]
    user_last_name = json_post["last_name"]
    print("using user role: ",user_role)
    try:
            this_user = User.objects.create_user(username=user_name,password=user_password,first_name=user_first_name,last_name=user_last_name)

            this_user.save()
            print(this_user)

            doctor = Doctors(user_id=this_user)
            doctor.save()

            hospital_user = HospitalUsers(user_id=this_user,user_role=user_role,role_group="medic")
            hospital_user.save()

            user_data = authUser(json_post)
            return user_data
            
    except Exception as e:
            print("okay: ",repr(e))
            return None


def createPatient(json_post):#create patient
    """
    Creates a new patient based on the provided JSON data.

    Args:
        json_post (dict): JSON data containing patient details.

    Returns:
        Patient object
    """
    user_name = json_post["user_name"]
    user_role = json_post["user_role"]
    user_password = json_post["user_password"]
    user_first_name = json_post["first_name"]
    user_last_name = json_post["last_name"]

    try:
        this_user = User.objects.create_user(username=user_name,password=user_password,first_name=user_first_name,last_name=user_last_name) #create user object

        this_user.save()
        print(this_user)

        patient = Patients(user_id=this_user)
        patient.save()
            
        hospital_user = HospitalUsers(user_id=this_user,user_role=user_role)
        hospital_user.save()

        user_data = authUser(json_post)
        return user_data
            
    except Exception as e:
            print("okay: ",repr(e))
            return None

@csrf_exempt
def reg_user(request):
    """
    Registers a new user based on the provided JSON data.

    Args:
        request: The HTTP request object.

    Returns:
        HTTPResponse of the result
    """
    json_post_str = request.body
    print("auth body: ", json_post_str)
    json_post = json.loads(json_post_str)
    
    user_name = json_post["user_name"]
    user_role = json_post["user_role"]
    user_type = json_post["user_type"]
    user_password = json_post["user_password"]
    user_first_name = json_post["first_name"]
    user_last_name = json_post["last_name"]

    if user_type == "non-medic":
        created_id,creation_status = createPatient(json_post)

        if creation_status != None:
            request.session["auth_man"] = created_id
            response_data =  ResponseMdl(200,"user login sucessful",creation_status)
            return HttpResponse(response_data.serial())
        else:
            return HttpResponse("User Already Registered")
    elif user_type == "medic":
        created_id,creation_status = createDoctor(json_post)

        if creation_status == None:
            return HttpResponse("User Already Registered")
        else:
            request.session["auth_man"] = created_id
            response_data =  ResponseMdl(200,"user login sucessful",creation_status)
            return HttpResponse(response_data.serial())
    else:
        response_data =  ResponseMdl(404,"user login unsucessful")
        return HttpResponse(response_data.serial())

    #print(json_post)
    #return HttpResponse("User Registered")

def mainPage(request):
        return TemplateResponse(request,"index.html")

def downloadsPage(request):
        file_name = "EdoctorUg.apk"
        file_path = os.path.join(BASE_DIR, "templates/edoctorUg.apk")
        return FileResponse(open(file_path,'rb'),file_name = file_name,content_type="application/*",as_attachment=False)
        #return TemplateResponse(request,"")