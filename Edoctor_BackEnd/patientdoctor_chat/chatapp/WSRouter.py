"""
Module for processing websockets javascript commands
"""

from django.contrib.sessions.backends.db import SessionStore
from importlib import import_module
from django.conf import settings
from chatapp.models import *
from chatapp.Models.ChatMsgModel import ChatMsgModel
#from chatapp.models import Patients
from asgiref.sync import sync_to_async, async_to_sync
from .UserDB import UserDB
from .WSResponseModel import WSResponseMdl
from channels.layers import get_channel_layer
import uuid
from datetime import date,time, datetime
class ChatRouter:
    """ Class for ChatRouter
    Parameters:
      chat_channel : being used by the router
      main_session_store : variable holding the http session store for this client
      chat_session_store : variable holding the websocket session store for this websocket connection
   
      chat_session_id : variable holding the current session key for this websocket connection 
      chat_to_channel : variable holding the doctors channel name incase the connected user is a patient
    
      chat_user_id : variable holding the current user id
      chat_channel_layer : variable holding the current chat layer being used in this websocket connection
      chat_user : variable holding the current user object
    """
    chat_channel = None
    main_session_store = None
    chat_session_store = None
    chat_session_id = ""
    chat_to_channel = ""

    chat_user_id = None
    chat_channel_layer = None

    chat_user = None

    def __init__(self,channel_name):
        """
        CONSTRUCTOR for the websocket router
        
        Parameters:
                channel_name (String) : Name of websocket used during this chat session
        
        Attributes:
                chat_channel (String) : Global websocket channel name used by this chat session
                
                main_session_store (SessionStore) : Global variable storing the Session Store used to keep the server's session keys
                
                chat_channel_layer (ChannelLayer) : Global variable storing the channel layer used during this websocket session
        """
        self.chat_channel = channel_name
        self.main_session_store = import_module(settings.SESSION_ENGINE).SessionStore
        self.chat_channel_layer = get_channel_layer()
        print("init chat router")
    
    async def route(self,chat_obj,consumer_obj):
        """
        Parse routes to the different json end points 
        
        Parameters:
        chat_obj (dictionary) : dictionary with the parsed json websocket message
        
        consumer_obj (Consumer) : Consumer object used for websocket send operations
        """
        chat_cmd = chat_obj["cmd"] #get current messsage type

        if chat_cmd == "auth":
            setup_fx = sync_to_async(self.setup) #call setup from async context
            auth_reply = await setup_fx(chat_obj)
            response_mdl = WSResponseMdl(200,"auth",auth_reply)
            return response_mdl.serial()
        elif chat_cmd =="set_online":
           self.setOnline(chat_obj)
        elif (chat_cmd == "get_online") and (self.chat_user!=None):
            if self.chat_user.user_role != "patient":
                #response_mdl = WSResponseMdl(500,"match","Doctor Waiting .... ")
                #print(adoctor_name,"\n")
                #return response_mdl.serial()
                 return None
            find_online = sync_to_async(self.findOnline)
            online_users = await find_online(chat_obj) #look for online doctors
            print("finding patient: ",self.chat_user_id)
            print("finding session id : ",self.chat_session_id)
            patient_object = await UserDB().getHospitalObject(self.chat_user_id)
            active_patient_x =  await UserDB().getUserObject(self.chat_user_id)
            init_patient_status = await (sync_to_async(lambda :self.resetPatient(active_patient_x)))()
            if len(online_users) <1:
                response_mdl = WSResponseMdl(500,"match","No Doctor Found")

                #print(adoctor_name,"\n")
                return response_mdl.serial() 
            print("\tall online users: ",online_users)

            for online_match in online_users:
                amatch_id = online_match["user_id_id"]
                active_user = await UserDB().getHospitalObject(self.chat_user_id)
                active_match = await UserDB().getHospitalObject(amatch_id) #get doctor object for the doctor to get assigned to
                current_user_names = await UserDB().getFullNames(self.chat_user_id)
                doctor_chat_details = {"full_names":current_user_names,"assigned_patient":self.chat_user_id,"chat_uuid":""}
                doctor_chat_json = WSResponseMdl(200,"verify_online","Patient Found",doctor_chat_details)
                self.chat_to_channel = await UserDB().getChannelName(active_match.id)
                #print(adoctor_name,"\n")
                #return response_mdl.serial()
                await self.chat_channel_layer.send(self.chat_to_channel,{"type": "raw_chat_message","text":doctor_chat_json.serial()})
            print("finished iterating online users")

        elif chat_cmd == "verify_match":
                if self.chat_user.user_role == "patient":
                #response_mdl = WSResponseMdl(500,"match","Doctor Waiting .... ")
                #print(adoctor_name,"\n")
                #return response_mdl.serial()
                    return None
                patient_id = chat_obj["message"]
                amatch_id = patient_id
                print("verifying patient: ",patient_id)
                active_user = await UserDB().getHospitalObject(self.chat_user_id)
                active_match = await UserDB().getHospitalObject(patient_id) #get patient object for the patient to get assigned to
                active_patient = await UserDB().getPatientObject(patient_id)
                active_patient_user = await UserDB().getUserObject(patient_id)
                active_doctor = await UserDB().getDoctorObject(self.chat_user_id)
                if (active_patient.pair_status==True):
                        doctor_chat_details = {"full_names":"","assigned_patient":patient_id,"chat_uuid":""}
                        doctor_chat_json = WSResponseMdl(500,"match","Patient Not Found",doctor_chat_details)
                        #print(adoctor_name,"\n")
                        #return response_mdl.serial()
                        #await self.chat_channel_layer.send(self.chat_to_channel,{"type": "raw_chat_message","text":doctor_chat_json.serial()}) #send message
                        return doctor_chat_json.serial()

                init_patient_status = await (sync_to_async(lambda :self.initPatient(active_patient_user,active_doctor)))() #init patient dataset
                if (init_patient_status==False):
                        patient_chat_details = {"full_names":"","assigned_patient":"","chat_uuid":""}
                        patient_chat_json = WSResponseMdl(500,"match","Patient Error",doctor_chat_details)
                        #print(adoctor_name,"\n")
                        #return response_mdl.serial()
                        #await self.chat_channel_layer.send(self.chat_to_channel,{"type": "raw_chat_message","text":doctor_chat_json.serial()}) #send message
                        return patient_chat_json.serial()
                await (sync_to_async(lambda :self.initDoctor(active_match,active_doctor)))()
                user_chat_uuid = await (sync_to_async(lambda :self.initChat(active_user,active_match)))() #save the assignment
                #await save_patient()
                #print("\t\tpatient object: ",active_patient)
                #doctor_object.assigned_patient = active_patient
                
                #save_assigned_doctor = sync_to_async(lambda: doctor_object.save())
                #await save_assigned_doctor()
                match_chat_uuid = await (sync_to_async(lambda :self.initChat(active_match,active_user)))()
                print(f"{user_chat_uuid} <--:::::--> {match_chat_uuid}")


                #assigned_doctor = await (sync_to_async(lambda :patient_object.assigned_doctor.user_id))()

                if (len(user_chat_uuid)<=0) and (len(match_chat_uuid)<=0):
                        doctor_chat_details = {"full_names":"","assigned_patient":patient_id,"chat_uuid":str(match_chat_uuid)}
                        doctor_chat_json = WSResponseMdl(500,"match","Patient Not Found",doctor_chat_details)
                        #print(adoctor_name,"\n")
                        #return response_mdl.serial()
                        #await self.chat_channel_layer.send(self.chat_to_channel,{"type": "raw_chat_message","text":doctor_chat_json.serial()}) #send message
                        return doctor_chat_json.serial()
                self.chat_to_channel = await UserDB().getChannelName(active_match.id)
                #print("assigned doctor", self.chat_to_channel)

                #online_user = await UserDB().getFullNames(self.chat_user_id)
                #doctor_response_mdl = WSResponseMdl(200,"match",online_user) #found online users

                #doctor_chat_json = doctor_response_mdl.serial() #online doctor reply
                current_user_names = await UserDB().getFullNames(self.chat_user_id)
            
                
                adoctor_name = await UserDB().getFullNames(amatch_id)
                online_meta = {"full_names":adoctor_name,"assigned_patient":"","chat_uuid":str(user_chat_uuid)}
                response_mdl = WSResponseMdl(200,"match","Doctor Found",online_meta)

                print(adoctor_name,"\n")
                await self.chat_channel_layer.send(self.chat_to_channel,{"type": "raw_chat_message","text":response_mdl.serial()}) #
                #return response_mdl.serial()


                doctor_chat_details = {"full_names":current_user_names,"assigned_patient":patient_id,"chat_uuid":str(match_chat_uuid)}
                doctor_chat_json = WSResponseMdl(200,"match","Patient Found",doctor_chat_details)
                #print(adoctor_name,"\n")
                #return response_mdl.serial()
                #await self.chat_channel_layer.send(self.chat_to_channel,{"type": "raw_chat_message","text":doctor_chat_json.serial()}) #send message
                return doctor_chat_json.serial()
        
            #print("\n\nOnline Doctors: ", online_doctors)
        elif chat_cmd == "chat":
                print("chat message")
                await self.sendMessage(chat_obj)
                return None
        elif chat_cmd == "book_appointment":
                if self.chat_user.user_role == "doctor":
                     return None
                elif self.chat_user.user_role == "patient":
                    xchan, appointment = await sync_to_async(lambda: self.bookAppointment(chat_obj))()
                    self.chat_channel_layer.send(xchan,{"type": "raw_chat_message","text":appointment.serial()})
                    return appointment.serial()
                print("book appointment")
        
        elif chat_cmd == "get_appointments":
            all_appointments = await sync_to_async( lambda: self.getAppointments(chat_obj))()
            appointments_no = len(all_appointments)
            if appointments_no>0:
                 response_mdl = WSResponseMdl(200,"appointments",f"{appointments_no} appointments",{"appointments_history":all_appointments})
                 await consumer_obj.send(text_data=response_mdl.serial())
            else:
                 response_mdl = WSResponseMdl(500,"appointments","no appointments")
                 await consumer_obj.send(text_data=response_mdl.serial())
                 
            print("getting appointments")
            return None
        
        elif chat_cmd == "get_prescriptions":
            all_prescriptions = await sync_to_async( lambda: self.getPrescriptions(chat_obj))()
            prescriptions_no = len(all_prescriptions)
            if prescriptions_no>0:
                 response_mdl = WSResponseMdl(200,"prescriptions",f"{prescriptions_no} prescriptions",{"prescriptions_history":all_prescriptions})
                 await consumer_obj.send(text_data=response_mdl.serial())
            else:
                 response_mdl = WSResponseMdl(500,"prescriptions","no prescriptions")
                 await consumer_obj.send(text_data=response_mdl.serial())
                 
            print("getting prescriptions")
            return None
        
        elif chat_cmd == "get_chats":
            all_chats = await sync_to_async( lambda: self.getChatHistory(chat_obj))()

            if len(all_chats)>0:
                 response_mdl = WSResponseMdl(200,"chat_history","okay",{"chat_history":all_chats})
                 await consumer_obj.send(text_data=response_mdl.serial())
            else:
                 response_mdl = WSResponseMdl(500,"chat_history","no chats")
                 await consumer_obj.send(text_data=response_mdl.serial())
                 
            print("getting appointments")
            return None

        elif chat_cmd == "order_item":
                await sync_to_async( lambda:self.orderItems(chat_obj))()
                response_mdl = WSResponseMdl(200,"order","order successful")
                await consumer_obj.send(text_data=response_mdl.serial())
                print("ordering item")
        
        elif chat_cmd == "prescribe":
                
                prescribe_status = await sync_to_async( lambda: self.prescribe(chat_obj))()
                response_mdl = WSResponseMdl(200,"prescribe",prescribe_status) #generate websocket prescription response

                await consumer_obj.send(text_data = response_mdl.serial()) #send websocket prescribe response to client
                print("prescribing drugs")

        #elif chat_cmd == "get_prescriptions":
        #        print("getting prescriptions")


        elif chat_cmd == "save_record":
                save_status = await sync_to_async( lambda: self.saveRecord(chat_obj))()
                response_mdl = WSResponseMdl(200,"save_record",save_status) #generate websocket prescription response

                await consumer_obj.send(text_data = response_mdl.serial()) #send websocket prescribe response to client
                print("prescribing drugs")


        elif chat_cmd == "order_drug":
            response_mdl = WSResponseMdl(500,"save_record","") #generate websocket prescription response

            await consumer_obj.send(text_data = response_mdl.serial())
            print("ordering drugs")

        elif chat_cmd == "get_orders":
                response_mdl = WSResponseMdl(200,"orders","No orders",{"orders_history":[]})
                await consumer_obj.send(text_data=response_mdl.serial())
                print("getting orders")

        elif chat_cmd == "get_records":
                all_records = await sync_to_async( lambda: self.getRecords(chat_obj))()

                if len(all_records)>0:
                    response_mdl = WSResponseMdl(200,"records","okay",{"records_history":all_records})
                    await consumer_obj.send(text_data=response_mdl.serial())
                else:
                    response_mdl = WSResponseMdl(500,"records","no records")
                    await consumer_obj.send(text_data=response_mdl.serial())
                 
                print("getting appointments")
                return None
                print("getting orders")
        
        elif chat_cmd == "labtest":
                
                labtest_status = await sync_to_async( lambda: self.makeLabTest(chat_obj))()
                response_mdl = WSResponseMdl(200,"labtest",labtest_status) #generate websocket prescription response

                await consumer_obj.send(text_data = response_mdl.serial()) 
                print("ordering labtest")

        elif chat_cmd == "get_labtests":
                labtests_status = await sync_to_async( lambda: self.getLabTests(chat_obj))()
                response_mdl = WSResponseMdl(200,"labtests","all labtests",{"labtests_history":labtests_status}) #generate websocket prescription response

                await consumer_obj.send(text_data = response_mdl.serial()) 
                print("getting labtests")
        print("routing request")

    def initChat(self,active_sender,active_receiver):
         """
            Initializes a chat between the active sender and receiver.

            Args:
                active_sender: The active sender of the chat.
                active_receiver: The active receiver of the chat.

            Returns:
                str: The chat UUID.
         """
    
         user_chats = Chats.objects.filter(sender = active_sender,receiver = active_receiver)

         if len(user_chats)==0:
            chat_model = Chats(sender = active_sender, receiver = active_receiver)
            chat_model.save()
            chat_uuid = chat_model.chat_uuid
            return str(chat_uuid)
         else:
              chat_uuid = user_chats[0].chat_uuid
              #return chat_uuid
              return str(chat_uuid)
    def initPatient(self,active_patient_x,active_medic):

        patient_object = Patients.objects.filter(user_id = active_patient_x, assigned_doctor = active_medic)#,receiver = active_receiver)

        if len(patient_object)==0:
            patient_model = Patients.objects.get(user_id = active_patient_x)
            patient_model.assigned_doctor = active_medic
            patient_model.pair_status = True
            patient_model.save()


            
            return True
        else:
              #chat_uuid = user_chats[0].chat_uuid
              #return chat_uuid
              return False
    def initDoctor(self,active_patient_hospital,active_medic):

        #patient_object = Patients.objects.filter(user_id = active_patient_x, assigned_doctor = active_medic)#,receiver = active_receiver)
        active_medic.assigned_patient = active_patient_hospital
        active_medic.save()

    def resetPatient(self,active_patient):
        #patient_object = Patients.objects.filter(user_id = active_patient, assigned_doctor = active_medic)#,receiver = active_receiver)

        #if len(patient_object)==0:
        patient_object = Patients.objects.get(user_id = active_patient)
        patient_object.assigned_doctor = None
        patient_object.pair_status = False
        patient_object.save()
            
        #    return True
        # else:
              #chat_uuid = user_chats[0].chat_uuid
              #return chat_uuid
        #      return False
        return True
    def setOnline(self, chat_obj):
         online_status = self.chat_obj["online_status"]
         user_object = async_to_sync( lambda: UserDB().getHospitalObject(self.chat_user_id))()
         user_object.online = chat_obj[online_status]
         user_object.save()

    def setup(self,chat_obj):
        self.chat_session_id = chat_obj["meta"]["session_id"] #get current session id from meta data
        self.chat_session_store = self.main_session_store(session_key=self.chat_session_id)#get current request session_id associated with current session id
        
        this_chat_uid = self.chat_session_store.get("auth_man") #get user id associated with this session key

        if this_chat_uid ==None:
            return "auth failed"
        self.chat_user_id = this_chat_uid
        print("chat user auth id: ",self.chat_user_id)
        self.chat_user = HospitalUsers.objects.get(user_id = self.chat_user_id) #get user associated with user id
        self.chat_user.online = True #set user online
        self.chat_user.channel_name = self.chat_channel #set current user channel
        self.chat_user.save() #save the changes
        print("current chat user", self.chat_user)
        return "auth okay"
    
    
    def delUser(self): #function to make user offline
        self.chat_user.online = False #user is offline
        self.chat_user.channel_name = "" #remove channel name
        self.chat_user.save() #save the changes
        print("user now offline")
    
    def findOnline(self,chat_obj): #look for online doctors
        doctor_type = chat_obj["message"] #doctor speciality to get
        chat_user_role = chat_obj["message"]
        online_users = HospitalUsers.objects.filter(user_role = chat_user_role, online=True).values() #find the 1st online doctor
        if(len(online_users)>0):
            return online_users
        return []
    
    def bookAppointment(self,chat_obj):

        appointment_details = chat_obj["meta"]
        raw_appointment_date = appointment_details["date"]
        raw_appointment_now_date = appointment_details["now_date"]
        print(raw_appointment_date)
        raw_appointment_now_time = appointment_details["now_time"]
        raw_appointment_time = appointment_details["time"]
        raw_appointment_note = appointment_details["note"]
        raw_appointment_chat_uuid = chat_obj["chat_uuid"]
        an_appointment_date = date.fromtimestamp(raw_appointment_date)

        print(an_appointment_date)
        an_appointment_time = time.fromisoformat(raw_appointment_time)
        print(an_appointment_time)

        now_appointment_date = date.fromtimestamp(raw_appointment_now_date)
        print(now_appointment_date)
        now_appointment_time = time.fromisoformat(raw_appointment_now_time)
        print(now_appointment_time)
        
        chats_user = Chats.objects.get(chat_uuid = raw_appointment_chat_uuid)
        assigned_user = chats_user.sender
        appointment = Appointments(appointment_setter = self.chat_user,appointment_with = assigned_user,appointment_date = an_appointment_date, appointment_time = an_appointment_time,appointment_initial_date = now_appointment_date, appointment_initial_time = now_appointment_time,appointment_details = raw_appointment_note)

        appointment.save()
        appointment_name = appointment.appointment_with.user_id.get_full_name()
        appointment_author = appointment.appointment_setter.user_id.get_full_name()
        appointment_dic = {
                  "appointment_with": appointment_name,
                  "appointment_author":appointment_author,
                  "appointment_uuid": str(appointment.appointment_uuid),
                  "appointment_time": str(appointment.appointment_time),
                  "appointment_initial_time":str(appointment.appointment_initial_time),
                  "appointment_date": str(appointment.appointment_date),
                  "appointment_initial_date":str(appointment.appointment_initial_date),
                  "appointment_note":appointment.appointment_details
             }
        channel_name = assigned_user.channel_name
        appointment_json = WSResponseMdl(200,"appointment","New Appointment",appointment_dic)
        #await self.chat_channel_layer.send(self.chat_to_channel,{"type": "raw_chat_message","text":appointment_json.serial()})
        #self.chat_channel_layer.send(channel_name,{"type": "raw_chat_message","text":appointment_json.serial()})
        return channel_name,appointment_json
        #pass

    """function that handles lab test"""
    def makeLabTest(self,chat_obj):
         """
         Creates a lab test entry in the database.

         Args:
            chat_obj (dict): The chat object containing lab test details.

         Returns:
            str: Confirmation message for successful lab test creation.
         """ 
         lab_test = chat_obj["meta"]
         tester_name = lab_test["test_personel"]
         test_name = lab_test["test_name"]
         print("\nLab Test: ",lab_test)

         doctor_object = (async_to_sync( lambda: UserDB().getDoctorObject(self.chat_user_id)))()
        
         assigned_hospital_patient = doctor_object.assigned_patient
         patient_user_id = assigned_hospital_patient.user_id
         patient_object = (async_to_sync( lambda: UserDB().getPatientObject(patient_user_id)))()
         
         lab_test = LabTest(test_name = test_name,assigned_test_doctor = doctor_object,assigned_test_patient = patient_object,test_details = tester_name)

         lab_test.save()

         return "LabTest Successful"
    
    def saveRecord(self,chat_obj):
        """save the patient record

        Args:
            chat_obj (_dictionary_): chat object with the websocket chat message json

        Returns:
            _String_: status message
        """         
         # This is the same as chat_obj ['meta'] except we have to convert the date and time to ISO
         
        record = chat_obj["meta"]
        chat_record_uuid = chat_obj["chat_uuid"]
        xrecord_title = record["record_title"]
        xrecord_details = record["record_details"]
        xrecord_date_str = record["record_date"]

        xrecord_time_str = record["record_time"]

        xrecord_date = date.fromisoformat(xrecord_date_str)
        xrecord_time = time.fromisoformat(xrecord_time_str)
        xrecord_timestamp = record["record_timestamp"]
        print("\nrecord: ",record)
        print("\n\trecord date: ",xrecord_date)
        print("\n\trecord time: ",xrecord_time)

        chats_user = Chats.objects.get(chat_uuid = chat_record_uuid)
        assigned_user = chats_user.sender
         
        patient_record = PatientRecords(record_author = self.chat_user,record_for = assigned_user, record_title = xrecord_title,record_details = xrecord_details,record_date = xrecord_date,record_time = xrecord_time,record_timestamp = xrecord_timestamp)

        patient_record.save()

        return "Patient Record Saved Successfully"
    
    """function handles order creation"""
    def orderItems(self,chat_obj):
         order_details = chat_obj["meta"]
         print("\nOrder details: ",order_details)
         order_cart = order_details["order_items"]
         order_chat_uuid = chat_obj["chat_uuid"]
         print("Using chat uuid: ",order_chat_uuid)
         order_receiver = self.chat_user
         if order_chat_uuid != None:
              active_chat_object = Chats.objects.get(chat_uuid = order_chat_uuid)
              order_receiver = active_chat_object.sender
              
         for order_item in order_cart:
            item_sku = order_item["item_sku"]
            item_data = ProductCatalog.objects.get(item_name = item_sku)
            item_owner = item_data.item_owner
            item_quantity = int(order_item["quantity" ])
            orders = Orders(quantity = item_quantity, item_name = item_data, assigned_pharmacy = item_owner,order_by=self.chat_user,recipient=order_receiver)
            orders.save()
         return "Order Successful"

    def prescribe(self,chat_obj):
        """get medicine details from chat_object"""
        medicine_details = chat_obj["meta"]
        chat_uuid  = chat_obj["chat_uuid"]
        print(medicine_details)
        medicine_name = medicine_details["medicine_name"] #medicine name
        medicine_dose = medicine_details["medicine_dose"] #medicine dosage

        
        #doctor_object = (async_to_sync( lambda: UserDB().getDoctorObject(self.chat_user_id)))()
        
        #assigned_hospital_patient = doctor_object.assigned_patient
        patient_object = Chats.objects.get(chat_uuid=chat_uuid).sender

        prescription = Prescriptions(prescribing_doctor = self.chat_user,prescribed_to_patient = patient_object,prescribed_medicine = medicine_name, prescribed_dose = medicine_dose)

        prescription.save()

        return "success"
        #pass
    
    def getAppointments(self,chat_obj):
        """
            Retrieves the appointments assigned to the user.

            Returns:
                QuerySet or list: The appointments assigned to the user.
        """
        hospital_user = (async_to_sync(lambda: UserDB().getHospitalObject(self.chat_user_id)))()
        created_appointments = Appointments.objects.filter(appointment_setter = hospital_user)
        invited_appointments = Appointments.objects.filter(appointment_with = hospital_user)

        all_appointments = []
        for created_appointment in created_appointments:
             appointment_name = created_appointment.appointment_with.user_id.get_full_name()
             appointment_dic = {
                  "appointment_with": appointment_name,
                  "appointment_uuid": str(created_appointment.appointment_uuid),
                  "appointment_time": str(created_appointment.appointment_time),
                  "appointment_initial_time":str(created_appointment.appointment_initial_time),
                  "appointment_date": str(created_appointment.appointment_date),
                  "appointment_initial_date":str(created_appointment.appointment_initial_date),
                  "appointment_note":created_appointment.appointment_details
             }
             all_appointments.append(appointment_dic)
             
        for invited_appointment in invited_appointments:
             appointment_name = invited_appointment.appointment_with.user_id.get_full_name()
             appointment_dic = {
                  "appointment_with": appointment_name,
                  "appointment_uuid": str(invited_appointment.appointment_uuid),
                  "appointment_time": str(invited_appointment.appointment_time),
                  "appointment_initial_time":str(invited_appointment.appointment_initial_time),
                  "appointment_date": str(invited_appointment.appointment_date),
                  "appointment_initial_date":str(invited_appointment.appointment_initial_date),
                  "appointment_note":invited_appointment.appointment_details
             }
             all_appointments.append(appointment_dic)
        print(all_appointments)
        return all_appointments
    
    def getRecords(self,chat_obj):
        """
            Retrieves the appointments assigned to the user.

            Returns:
                QuerySet or list: The appointments assigned to the user.
        """
        hospital_user = (async_to_sync(lambda: UserDB().getHospitalObject(self.chat_user_id)))()

        user_records = []

        if self.chat_user.user_role !="patient":
            user_records = PatientRecords.objects.filter(record_author = hospital_user)
        else:
            user_records = PatientRecords.objects.filter(record_for = hospital_user)

        all_records = []
        for user_record in user_records:
             record_for = user_record.record_for.user_id.get_full_name()
             record_author = user_record.record_author.user_id.get_full_name()
             record_dic = {
                  "record_title": user_record.record_title,
                  "record_author": record_author,
                  "record_for": record_for,
                  "record_uuid": str(user_record.record_uuid),
                  "record_time": str(user_record.record_time),
                  "record_date": str(user_record.record_date),
                  "record_details":user_record.record_details
             }
             all_records.append(record_dic)
             
        
        print(all_records)
        return all_records

    
    def getLabTests(self,chat_obj):
        """
            Retrieves the appointments assigned to the user.

            Returns:
                QuerySet or list: The appointments assigned to the user.
        """
        hospital_user = (async_to_sync(lambda: UserDB().getHospitalObject(self.chat_user_id)))()

        lab_tests = []

        if self.chat_user.user_role !="patient":
            doctor_user = (async_to_sync(lambda: UserDB().getDoctorObject(self.chat_user_id)))()
            lab_tests = LabTest.objects.filter(assigned_test_doctor = doctor_user)
        else:
            patient_user = (async_to_sync(lambda: UserDB().getPatientObject(self.chat_user_id)))()
            lab_tests = LabTest.objects.filter(assigned_test_patient = patient_user)

        all_labtests = []
        for lab_test in lab_tests:
             test_uuid = str(lab_test.test_uuid)
             test_name = lab_test.test_name
             test_for = lab_test.assigned_test_patient.user_id.get_full_name()
             test_author = lab_test.assigned_test_doctor.user_id.get_full_name()
             test_details = lab_test.test_details
             test_results = lab_test.test_results
             test_date = str(lab_test.test_date)

             test_dic = {
             "labtest_uuid":test_uuid,
             "labtest_name":test_name,
             "labtest_for":test_for,
             "labtest_author":test_author,
             "labtest_details":test_details,
             "labtest_results":test_results,
             "labtest_date":test_date
             }
             all_labtests.append(test_dic)
             

        print(all_labtests)
        return all_labtests
    
    def getPrescriptions(self,chat_obj):
        """
            Retrieves the prescriptions assigned to the user.

            Returns:
                QuerySet or list: The prescriptions assigned to the user.
        """
        hospital_user = (async_to_sync(lambda: UserDB().getHospitalObject(self.chat_user_id)))()

        user_prescriptions = []

        if self.chat_user.user_role !="patient":
            user_prescriptions = Prescriptions.objects.filter(prescribing_doctor = hospital_user)
        else:
            user_prescriptions = Prescriptions.objects.filter(prescribed_to_patient = hospital_user)

        all_prescriptions = []
        for user_prescription in user_prescriptions:
             prescribed_for = user_prescription.prescribed_to_patient.user_id.get_full_name()
             prescribed_by = user_prescription.prescribing_doctor.user_id.get_full_name()
             prescription_dic = {
                  "prescribed_by": prescribed_by,
                  "prescribed_for": prescribed_for,
                  "prescription_id": str(user_prescription.prescription_id),
                  "prescription_date": str(user_prescription.prescription_date),
                  "prescription_note":user_prescription.notes,
                  "prescription_medicine":user_prescription.prescribed_medicine,
                  "prescription_dosage":user_prescription.prescribed_dose
             }
             all_prescriptions.append(prescription_dic)
             
        
        print(all_prescriptions)
        return all_prescriptions
    
    def getChatHistory(self,chat_obj):
            """
            Retrieves the chat history associated with the given chat object.

            Args:
                chat_obj: The chat object for which the chat history is to be retrieved.

            Returns:
                list: The chat history.
            """
            user_object = (async_to_sync(lambda: UserDB().getHospitalObject(self.chat_user_id)))()
            chats_history = Chats.objects.filter(receiver = user_object)
            if chats_history == None:
                 return []
            user_chats = []
            for chat_history in chats_history:
                chat_object = chat_history.chat_data
                recv_object = chat_history.sender

                #recv_chat_object = Chats.objects.get(sender = recv_object, receiver=user_object)

                #recv_uuid = recv_chat_object.chat_uuid
                chat_uuid = chat_history.chat_uuid

                chat_recv_id = recv_object.user_id.id
                chat_recv_names = (async_to_sync(lambda: UserDB().getFullNames(chat_recv_id)))()
                #chat_sum = {"chat_time_date":chat_object["chat_time"],"chat_name":chat_recv_names}
                chat_sum = {"full_names":chat_recv_names,"assigned_patient":"","chat_uuid":str(chat_uuid),"chat_time":str(datetime.fromtimestamp(chat_object["chat_time"]))}
                chat_details = {"summary":chat_sum,"history":chat_object["chat_data"]}
                user_chats.append(chat_details)
                print(chat_details)
            print(user_chats)
            return user_chats


    def storeChat(self,chat_obj):
        """
        Stores a chat message in the database.

        Args:
            chat_obj (dict): The chat object containing message details.

        Returns:
            str: The channel name of the chat sender.
        """
        chat_message = chat_obj["message"]
        chat_time = chat_obj["chat_time"]
        chat_type = chat_obj["chat_type"]

        active_chat_uuid = uuid.UUID(chat_obj["chat_uuid"]).hex
        print("finding uuid: ",active_chat_uuid)
        active_chat_object = Chats.objects.get(chat_uuid = active_chat_uuid)

        active_chat_sender = active_chat_object.sender
        active_chat_recv = active_chat_object.receiver

        
        
        active_chat_sender_channel = active_chat_sender.channel_name
        return active_chat_sender_channel

    async def sendMessage(self,chat_obj):
        """function to send a message

        Args:
            chat_obj (__dictionary__): chat_object
        """
        chat_message = chat_obj["message"]
        this_chat_uuid = chat_obj["chat_uuid"]
        print("finding this uuid: ",this_chat_uuid)
        active_chat_uuid = uuid.UUID(this_chat_uuid).hex
        print("finding uuid: ",active_chat_uuid)
        active_chat_object =await (sync_to_async(lambda: Chats.objects.get(chat_uuid = active_chat_uuid)))()
        print("\tactive_chat_object: ",active_chat_object)
        active_chat_sender = await (sync_to_async(lambda: active_chat_object.sender))()
        print("\tactive_chat_sender: ",active_chat_sender)
        active_chat_sender_channel = active_chat_sender.channel_name

        #get the chat object related to the thid user 
        recv_object = await (sync_to_async(lambda: Chats.objects.get(sender = active_chat_object.receiver, receiver=active_chat_object.sender)))()

        recv_uuid = await (sync_to_async(lambda: recv_object.chat_uuid))()

        print("\t sending data to: ", recv_uuid)
        await self.chat_channel_layer.send(active_chat_sender_channel,{"type": "chat_message","text":chat_message,"uuid":str(recv_uuid)})
        chat_msg = ChatMsgModel(0,chat_message,0)

        active_chat_object.chat_data["chat_data"].append(chat_msg.__dict__)
        await (sync_to_async(lambda: active_chat_object.save()))()

        chat_msg = ChatMsgModel(1,chat_message,0)
        recv_object.chat_data["chat_data"].append(chat_msg.__dict__)
        await (sync_to_async(lambda: recv_object.save()))()

        #if self.chat_user.user_role == "patient":
        #    response_mdl = WSResponseMdl(200,"chat",chat_message)

        #    chat_json = response_mdl.serial()
        #    await self.chat_channel_layer.send(self.chat_to_channel,{"type": "chat_message","text":chat_message})
        #    print("\n\tsent message")
        
        #elif self.chat_user.user_role == "doctor":
        #    doctor_object = await UserDB().getDoctorObject(self.chat_user_id)
        #    assigned_patient_id = await (sync_to_async(lambda :doctor_object.assigned_patient.user_id))()
            #doctor_object.assigned_patient
        #    print("\tusing assigned patient id: ", assigned_patient_id)
        #    assigned_patient_channel = await UserDB().getChannelName(assigned_patient_id)

        #    print("\n\nsending to assigned patient: ",assigned_patient_channel)
            
        #    await self.chat_channel_layer.send(assigned_patient_channel,{"type": "chat_message","text":chat_message})
        #    pass

    async def sendOpenMessage(self,aws_channel,str_msg):
        """
        Sends an open message to the specified AWS channel asynchronously.

        Args:
            aws_channel (str): The AWS channel to which the message will be sent.
            str_msg (str): The message to be sent.

        Returns:
            None
        """
        await self.chat_channel_layer.send(self.aws_channel,{"type": "raw_chat_message","text":str_msg,"code":500}) #send message
        pass
        



