
# This is the heart of the hospital. We need to be able to create a User object in the Auth
from django.db import models
from django.contrib.auth.models import User
import uuid
from time import time
from datetime import datetime
# Create your models here.

class HospitalUsers(models.Model):
    """
    Table representing all the users in the hospital
    
      Attributes:
           user_id ( User foreignkey) : The user id linked to the Auth user table
           user_role (CharField) : role of the user at the hospital
           online (BooleanField) : online status of the user
           channel_name (CharField) : the websocket channel name being used by the current use
    
    """
    user_id = models.ForeignKey(User,unique = True,on_delete = models.CASCADE)
    user_role = models.CharField(max_length = 255)
    role_group = models.CharField(max_length = 255, default = "visitor")
    online = models.BooleanField(default=False)
    channel_name = models.CharField(default = "", max_length = 255)


class Doctors(models.Model):
    """
    Table representing all the Doctor roles in the hospital
    
      Attributes:
           user_id ( User foreignkey) : The user id linked to the Auth user table
           speciality (CharField) : doctor's medical field at the hospital
           assigned_patient (HospitalUsers ForeignKey) : patient the doctor is assigned to
    
    """
    user_id = models.ForeignKey(User,unique = True,on_delete = models.CASCADE, null = True)
    speciality = models.CharField(default = "consultant", max_length = 255)
    assigned_patient = models.ForeignKey(HospitalUsers, on_delete = models.CASCADE, null=True)
    
class Patients(models.Model):
    """
    Table representing all the users in the hospital
    
      Attributes:
           user_id ( User foreignkey) : The user id linked to the Auth user table     
           assigned_doctor (Doctors ForeignKey) : the doctor the patient is assigned to
    
    """
    user_id = models.ForeignKey(User,unique=True, on_delete = models.CASCADE)
    assigned_doctor = models.ForeignKey(Doctors, on_delete = models.CASCADE, null=True)
    pair_status = models.BooleanField(default=False)

class Specialities(models.Model):
    """
    Table representing all the supported medical fields at the hospital
    
      Attributes:
           speciality (CharFeld) : The name of the medical field
           related_terms (Doctors ForeignKey) : The medical terms this specialty is related to
    
    """
    speciality_name = models.CharField(default = "Physician",max_length = 255)
    related_terms = models.JSONField()

class Appointments(models.Model):
    """
    Table representing all the appointments at the hospital
    
      Attributes:
           appointment_user (Patients ForeignKey) : The patient booking an appointment 
           appointment_doctor (Doctors ForeignKey) : the doctor the patient is assigned to  
    """
    appointment_uuid = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False) # Returns a field to be used as a primary key in the chat_id
    appointment_setter = models.ForeignKey(HospitalUsers,related_name = "appointment_setter",null = True, on_delete = models.CASCADE)
    appointment_with = models.ForeignKey(HospitalUsers, related_name = "appointment_with", null = True, on_delete = models.CASCADE)
    appointment_date = models.DateField(null = True)
    appointment_time = models.TimeField(null = True)
    appointment_initial_date = models.DateField(null = True)
    appointment_initial_time = models.TimeField(null = True)
    appointment_details = models.CharField(default = "", max_length = 255)


class Pharmacies(models.Model):
    """
    Table representing all the registerd pharmacies
    
      Attributes:
           pharmacy_name (CharField) : The name of the pharmacy  
           pharmacy_personel (ForeignKey) : HospitalUsers user responsible for the pharmacy
    
    """
    pharmacy_name = models.CharField(default = "",max_length = 255)
    pharmacy_personel = models.ForeignKey(HospitalUsers,on_delete = models.CASCADE)


class ProductCatalog(models.Model):
    """This class represents a product catalog with fields for item name, owner, available amount, sold, amount, and unit price.

    Args:
        models ([type]): [description]
    """
    item_name = models.CharField(default = "", max_length = 255)
    item_owner = models.ForeignKey(HospitalUsers, on_delete = models.CASCADE)
    item_available_amount = models.IntegerField(default = 0)
    item_sold_amount = models.IntegerField(default = 0)
    item_unit_price = models.IntegerField(default = 0)

class Orders(models.Model):
    """
    Model representing a drug order.

    Attributes:
        quantity (IntegerField): The quantity of the drug being ordered.
        item_name (ForeignKey): The name of the drug being ordered.
        assigned_pharmacy (ForeignKey): The pharmacy responsible for the order.
        recipient (ForeignKey): The patient recipient of the order.
        delivery_man (ForeignKey): The hospital user responsible for delivery.
    """
    order_uuid = models.UUIDField(unique = True,default = uuid.uuid4, editable = False) # Returns a field to be used as a primary key in the 
    quantity = models.IntegerField(default = 1)
    item_name = models.ForeignKey(ProductCatalog, on_delete = models.CASCADE, null = True)
    ordered_by = models.ForeignKey(HospitalUsers,null = True,  related_name = "ordered_by", on_delete = models.CASCADE)
    assigned_pharmacy = models.ForeignKey(HospitalUsers, related_name = "assigned_pharma",on_delete = models.CASCADE, null = True)
    recipient = models.ForeignKey(HospitalUsers, related_name = "recipient", on_delete = models.CASCADE, null = True)
    delivery_man =  models.ForeignKey(HospitalUsers, related_name = "delivery_man", on_delete = models.CASCADE,null = True)
#class Order(models.Model):
#    order_uuid = models.UUIDField(unique = True,default = uuid.uuid4, editable = False) # Returns a field to be used as a primary key in the chat_id
#    ordered_by = models.ForeignKey(HospitalUsers, related_name = "ordered_by", on_delete = models.CASCADE)
#    ordered_for = models.ForeignKey(HospitalUsers, related_name = "ordered_for", on_delete = models.CASCADE)

class Prescriptions(models.Model):
    prescription_id = models.UUIDField(default = uuid.uuid4, unique = True)
    prescribing_doctor = models.ForeignKey(HospitalUsers,related_name = "prescribing_doctor",null = True,on_delete = models.CASCADE)
    prescribed_to_patient = models.ForeignKey(HospitalUsers,related_name = "prescribing_patient",null = True,on_delete = models.CASCADE)
    prescribed_medicine = models.CharField(default = "",max_length = 255)
    prescribed_dose = models.CharField(default = "",max_length = 255)
    notes = models.CharField(default = "Medicine", max_length = 255)
    prescription_date = models.DateField(default = datetime.now())
    #order = models.ForeignKey(OrderDrugs,on_delete = models.CASCADE, null = True)

class LabTest(models.Model):
    assigned_test_doctor = models.ForeignKey(Doctors,on_delete = models.CASCADE)
    assigned_test_patient = models.ForeignKey(Patients,on_delete = models.CASCADE)
    test_details = models.CharField(default = "",max_length = 255)
    

class PatientRecords(models.Model):
    """
    Model representing a medical record.

    Attributes:
        patient (ForeignKey): The patient associated with the record.
        doctor (ForeignKey): The doctor associated with the record.
        record_title (CharField): The title of the record.
        record_details (CharField): The details of the record.
        record_date (DateField): The date of the record.
        record_time (TimeField): The time of the record.
        record_timestamp (PositiveBigIntegerField): The timestamp of the record.
    """
    record_for = models.ForeignKey(HospitalUsers, null = True,related_name="record_for_user",on_delete = models.CASCADE)
    record_author = models.ForeignKey(HospitalUsers,null = True,related_name="record_by_user",on_delete = models.CASCADE)
    record_title = models.CharField(default = "", max_length = 255)
    record_details = models.CharField(default = "", max_length = 255)
    record_date = models.DateField(null = True)
    record_time = models.TimeField(null = True)
    record_timestamp = models.PositiveBigIntegerField(default = 0)
    record_uuid = models.UUIDField(unique = True,default = uuid.uuid4, editable = False) # Returns a field to be used as a primary key in the chat_id

class Chats(models.Model):
    """
    Model representing a chat between a patient and a doctor.

    Attributes:
        chat_uuid (UUIDField): The unique identifier for the chat.
        patient (ForeignKey): The patient participating in the chat.
        doctor (ForeignKey): The doctor participating in the chat.
    """

    chat_uuid = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False) # Returns a field to be used as a primary key in the chat_id
    # Set foreign key on hospital_patient to avoid duplication of
    sender = models.ForeignKey(HospitalUsers,related_name = "hospital_sender", on_delete = models.CASCADE, null = True)
    receiver = models.ForeignKey(HospitalUsers,related_name = "hospital_receiver", on_delete = models.CASCADE, null = True)
    chat_data = models.JSONField(default = {"chat_data":[],"chat_time":int(time())})