package patientdoctorwebsockets;

import okhttp3.OkHttpClient;
import okhttp3.WebSocketListener;

import patientdoctorwebsockets.Models.*;

/*
import patientdoctorwebsockets.Models.WSModels.WSAuthModel;
import patientdoctorwebsockets.Models.WSModels.WSChatDataModel;
import patientdoctorwebsockets.Models.WSModels.WSChatMsgModel;
import patientdoctorwebsockets.Models.WSModels.WSSessionModel;
import patientdoctorwebsockets.Models.WSModels.WSAppointmentModel;
import patientdoctorwebsockets.Models.WSModels.WSMedicineModel;
import patientdoctorwebsockets.Models.WSModels.WSLabTestModel;
import patientdoctorwebsockets.Models.WSModels.WSOrderModel;
import patientdoctorwebsockets.Models.WSModels.WSOrderModel;
*/

import patientdoctorwebsockets.Models.WSModels.*;
import patientdoctorwebsockets.Httpman;

import java.time.LocalTime;
import java.time.Instant;
import java.time.LocalDate;


//class to handle network requests to the hospital backend
public class Hospitalman 
{
    String hospital_url = "127.0.0.1"; //localhost
    //String hospital_url = "192.168.1.152";//Hospital server URL 
    int hospital_port = 8000; //Hospital server port
    Httpman hospital_Client; //OKHttpClient to use for connections to the hospital server

    public int con_ctx = 0;
    public Hospitalman(String aurl,int aport)
    {
        hospital_url = aurl;
        hospital_port = aport;
        hospital_Client = new Httpman(hospital_url, hospital_port); //make Httpman object to handle the http connections
    }

    public AuthResponse register(RegistrationModel registration_model) //register user using details from the Registration Model
    {
        String hospital_register_path = "/chatapp/register/"; //path to the registration endpoint at the hospital server
        String registration_string_data = registration_model.toJson(); //serialize the contents of the registration model into a json string.

        String response_data = hospital_Client.send(registration_string_data, hospital_register_path); //send registration request to server end point.
        if(response_data!=null)
        {
            
            AuthResponse parse_result = AuthResponse.deJson(response_data);

            if(parse_result!=null)
            {
            //System.out.println(parse_result.meta_data.names);
            //System.out.println(parse_result.status_msg);
            return parse_result;
            }
        }

        return null;
    }

    public AuthResponse auth(AuthModel auth_model) //method implementing hospital server login
    {
        String hospital_auth_path = "/chatapp/auth/"; //path to the login endpoint at the hospital server
        String auth_string_data = auth_model.toJson(); //serialize the contents of the auth model into a json string.

        String response_data = hospital_Client.send(auth_string_data, hospital_auth_path); //send login request to server end point.

        con_ctx = con_ctx+5;
        if(response_data!=null)
        {
            
            AuthResponse parse_result = AuthResponse.deJson(response_data);

            if(parse_result!=null)
            {
            ////System.out.println(parse_result.meta_data.names);
            ////System.out.println(parse_result.status_msg);
            return parse_result;
            }
        }

        return null;
    }

    public boolean authWebSocket(WebSocketListener webSocketListener)
    {
        WSAuthModel ws_authmodel = new WSAuthModel();
        ws_authmodel.cmd = "auth";
        ws_authmodel.message = "hello";
        ws_authmodel.meta = new WSSessionModel();

       ((WSSessionModel)ws_authmodel.meta).session_id = hospital_Client.getCookie("sessionid");
        
        String ws_authmodel_str = ws_authmodel.toJson();

        System.out.println("\n\nsend ws socket: "+ws_authmodel_str);
        hospital_Client.initWebSocket("/ws/chat/",webSocketListener);
        boolean ws_status = hospital_Client.wsSend(ws_authmodel_str);


        con_ctx = con_ctx+5;
        return ws_status;
        

        
    }

    public String getSessionId()
    {

        return  hospital_Client.getCookie("sessionid");
    }

    public boolean authWebSocket(WebSocketListener webSocketListener,String session_id)
    {
        WSAuthModel ws_authmodel = new WSAuthModel();
        ws_authmodel.cmd = "auth";
        ws_authmodel.message = "hello";
        WSSessionModel ws_sesson_model = new WSSessionModel();
        ws_sesson_model.session_id = session_id;
        ws_authmodel.meta = ws_sesson_model;


        System.out.println("\t\tsesson id being used: "+session_id);
        String ws_authmodel_str = ws_authmodel.toJson();

        System.out.println("\n\nsend ws socket: "+ws_authmodel_str);
        hospital_Client.initWebSocket("/ws/chat/",webSocketListener);
        boolean ws_status = hospital_Client.wsSend(ws_authmodel_str);



        return ws_status;



    }

    public void findOnlineDoc()
    {
        WSChatDataModel ws_chat_data_model = new WSChatDataModel(); //create chat model
        ws_chat_data_model.cmd = "get_online"; //use the get_online command
        ws_chat_data_model.message = "consultant"; //dummy message

        String ws_chat_data_model_str = ws_chat_data_model.toJson(); //convert the model to json string

        ////System.out.println(" sending find: "+ ws_chat_data_model_str);

        hospital_Client.wsSend(ws_chat_data_model_str);
    }

    public void findOnlineDoc(String speciality)
    {
        WSChatDataModel ws_chat_data_model = new WSChatDataModel(); //create chat model
        ws_chat_data_model.cmd = "get_online"; //use the get_online command
        ws_chat_data_model.message = speciality; //dummy message

        String ws_chat_data_model_str = ws_chat_data_model.toJson(); //convert the model to json string

        ////System.out.println(" sending find: "+ ws_chat_data_model_str);

        hospital_Client.wsSend(ws_chat_data_model_str);
    }

    /**
     * getAppointments
     */
    public void getAppointments()
    {
        WSChatDataModel ws_chat_data_model = new WSChatDataModel(); //create chat model
        ws_chat_data_model.cmd = "get_appointments"; //use the get_online command
        ws_chat_data_model.message = "consultant"; //dummy message

        String ws_chat_data_model_str = ws_chat_data_model.toJson(); //convert the model to json string

        ////System.out.println(" sending find: "+ ws_chat_data_model_str);

        hospital_Client.wsSend(ws_chat_data_model_str);
    }


    public void getRecords()
    {
        WSChatDataModel ws_chat_data_model = new WSChatDataModel(); //create chat model
        ws_chat_data_model.cmd = "get_records"; //use the get_online command
        ws_chat_data_model.message = "consultant"; //dummy message

        String ws_chat_data_model_str = ws_chat_data_model.toJson(); //convert the model to json string

        ////System.out.println(" sending find: "+ ws_chat_data_model_str);

        hospital_Client.wsSend(ws_chat_data_model_str);
    }

    public void getPrescriptions()
    {
        WSChatDataModel ws_chat_data_model = new WSChatDataModel(); //create chat model
        ws_chat_data_model.cmd = "get_prescriptions"; //use the get_online command
        ws_chat_data_model.message = "consultant"; //dummy message

        String ws_chat_data_model_str = ws_chat_data_model.toJson(); //convert the model to json string

        ////System.out.println(" sending find: "+ ws_chat_data_model_str);

        hospital_Client.wsSend(ws_chat_data_model_str);
    }

    public void getChatHistory()
    {
        WSChatDataModel ws_chat_data_model = new WSChatDataModel(); //create chat model
        ws_chat_data_model.cmd = "get_chats"; //use the get_online command
        ws_chat_data_model.message = "consultant"; //dummy message

        String ws_chat_data_model_str = ws_chat_data_model.toJson(); //convert the model to json string

        ////System.out.println(" sending find: "+ ws_chat_data_model_str);

        hospital_Client.wsSend(ws_chat_data_model_str);
    }

    public void makeAppointment(long appointment_date,LocalTime appointment_time)
    {
        
        System.out.println("Appointment: "+appointment_date+" appointment time: "+appointment_time);

        WSAppointmentModel ws_appointment_model = new WSAppointmentModel();
        ws_appointment_model.date = appointment_date;
        ws_appointment_model.now_date = Instant.now().getEpochSecond();
        ws_appointment_model.time = appointment_time.toString();
        ws_appointment_model.now_time = LocalTime.now().toString();

        String str_appointment_model = ws_appointment_model.toJson();
        System.out.println("Appointment object: "+str_appointment_model);

        WSChatMsgModel wsChatDataModel = new WSChatMsgModel();
        wsChatDataModel.cmd = "book_appointment";
        wsChatDataModel.message = "booking";
        wsChatDataModel.meta =(WSAppointmentModel) ws_appointment_model;
        String ws_chat_data_model = wsChatDataModel.toJson();

        hospital_Client.wsSend(ws_chat_data_model);
    }

    public void makeAppointment(String doc_chat_uuid, String appointment_note,long appointment_date,LocalTime appointment_time)
    {
        
        System.out.println("Appointment: "+appointment_date+" appointment time: "+appointment_time);

        WSAppointmentModel ws_appointment_model = new WSAppointmentModel();
        ws_appointment_model.date = appointment_date;
        ws_appointment_model.now_date = Instant.now().getEpochSecond();
        ws_appointment_model.time = appointment_time.toString();
        ws_appointment_model.now_time = LocalTime.now().toString();
        ws_appointment_model.note = appointment_note;

        String str_appointment_model = ws_appointment_model.toJson();
        System.out.println("Appointment object: "+str_appointment_model);

        WSChatMsgModel wsChatDataModel = new WSChatMsgModel();
        wsChatDataModel.cmd = "book_appointment";
        wsChatDataModel.message = "booking";
        wsChatDataModel.chat_uuid = doc_chat_uuid;
        wsChatDataModel.meta =(WSAppointmentModel) ws_appointment_model;
        String ws_chat_data_model = wsChatDataModel.toJson();

        hospital_Client.wsSend(ws_chat_data_model);
    }

    /**
     * function to make a prescription
     * @param medicine_name name of the medicine
     * @param medicine_dose dosage of the medicine
     */
    public void makePrescription(String medicine_name,String medicine_dose)
    {
        

        WSMedicineModel ws_medicine_model = new WSMedicineModel();
        ws_medicine_model.medicine_name = medicine_name;
        ws_medicine_model.medicine_dose = medicine_dose;
        

        String str_medicine_model = ws_medicine_model.toJson();
        

        WSChatMsgModel wsChatDataModel = new WSChatMsgModel();
        wsChatDataModel.cmd = "prescribe";
        wsChatDataModel.message = "prescribe_drug";
        wsChatDataModel.meta =(WSMedicineModel) ws_medicine_model;
        String ws_chat_data_model = wsChatDataModel.toJson();

        hospital_Client.wsSend(ws_chat_data_model);
    }

    public void makePrescription(String chat_uuid, String medicine_name,String medicine_dose)
    {
        

        WSMedicineModel ws_medicine_model = new WSMedicineModel();
        ws_medicine_model.medicine_name = medicine_name;
        ws_medicine_model.medicine_dose = medicine_dose;
        

        String str_medicine_model = ws_medicine_model.toJson();
        

        WSChatMsgModel wsChatDataModel = new WSChatMsgModel();
        wsChatDataModel.cmd = "prescribe";
        wsChatDataModel.message = "prescribe_drug";
        wsChatDataModel.chat_uuid = chat_uuid;
        wsChatDataModel.meta =(WSMedicineModel) ws_medicine_model;
        String ws_chat_data_model = wsChatDataModel.toJson();

        hospital_Client.wsSend(ws_chat_data_model);
    }

    /**
     * function that saves the patient record
     * @param record_title title of the record
     * @param record_details details of the patient record
     */
    public void saveRecord(String record_title,String record_details)
    {
        

        WSPatientRecordModel ws_patient_record_model = new WSPatientRecordModel(record_title,record_details);

        String str_patient_record_model = ws_patient_record_model.toJson();
        

        WSChatMsgModel wsChatDataModel = new WSChatMsgModel();
        wsChatDataModel.cmd = "save_record";
        wsChatDataModel.message = "save patient record";
        wsChatDataModel.meta =(WSPatientRecordModel) ws_patient_record_model;
        String ws_chat_data_model = wsChatDataModel.toJson();

        hospital_Client.wsSend(ws_chat_data_model);
    }

    /**
     * function that saves the patient record
     * @param record_title title of the record
     * @param record_details details of the patient record
     */
    public void saveRecord(String chat_uuid,String record_title,String record_details)
    {
        

        WSPatientRecordModel ws_patient_record_model = new WSPatientRecordModel(record_title,record_details);

        String str_patient_record_model = ws_patient_record_model.toJson();
        

        WSChatMsgModel wsChatDataModel = new WSChatMsgModel();
        wsChatDataModel.cmd = "save_record";
        wsChatDataModel.message = "save patient record";
        wsChatDataModel.chat_uuid = chat_uuid;
        wsChatDataModel.meta =(WSPatientRecordModel) ws_patient_record_model;
        String ws_chat_data_model = wsChatDataModel.toJson();

        hospital_Client.wsSend(ws_chat_data_model);
    }

    public void makeLabTest(String test_name,String test_personel)
    {
        
        System.out.println("Appointment: "+test_name+" appointment time: "+test_personel);

        WSLabTestModel ws_labtest_model = new WSLabTestModel();
        ws_labtest_model.test_name = test_name;
        ws_labtest_model.test_personel = test_personel;
        

        String str_lab_test_model = ws_labtest_model.toJson();
        

        WSChatMsgModel wsChatDataModel = new WSChatMsgModel();
        wsChatDataModel.cmd = "labtest";
        wsChatDataModel.message = "Lab Test";
        wsChatDataModel.meta =(WSLabTestModel) ws_labtest_model;
        String ws_chat_data_model = wsChatDataModel.toJson();

        hospital_Client.wsSend(ws_chat_data_model);
    }


    public void orderItem(String med_name,Integer med_quantity, String pharma_id)
    {
        
        

        WSOrderModel ws_order_model = new WSOrderModel(med_name,med_quantity,pharma_id);

        String str_order_model = ws_order_model.toJson();
        

        WSChatMsgModel wsChatDataModel = new WSChatMsgModel();
        wsChatDataModel.cmd = "order_item";
        wsChatDataModel.message = "Creating Order....";
        wsChatDataModel.meta =(WSOrderModel) ws_order_model;
        String ws_chat_data_model = wsChatDataModel.toJson();

        hospital_Client.wsSend(ws_chat_data_model);
    }

    public boolean chatWebSocket(String message)
    {
        WSChatDataModel wsChatDataModel = new WSChatDataModel();
        wsChatDataModel.cmd = "chat";
        wsChatDataModel.message = message;

        String ws_chat_data_model = wsChatDataModel.toJson();

        hospital_Client.wsSend(ws_chat_data_model);
        return false;
    }

    
    public boolean makeOrder(OrderItemModel order_cart[])
    {
        OrderModel order_model = new OrderModel(order_cart);
        

        WSChatMsgModel wsChatDataModel = new WSChatMsgModel();
        wsChatDataModel.cmd = "order_items";
        wsChatDataModel.message = "Creating Order....";
        wsChatDataModel.meta =(OrderModel) order_model;
        String ws_chat_data_model = wsChatDataModel.toJson();

        hospital_Client.wsSend(ws_chat_data_model);
        return true;
    }

    public boolean chatWebSocket(String message,String chat_uuid)
    {
        WSChatDataModel wsChatDataModel = new WSChatDataModel();
        wsChatDataModel.cmd = "chat";
        wsChatDataModel.chat_uuid = chat_uuid;
        wsChatDataModel.message = message;

        String ws_chat_data_model = wsChatDataModel.toJson();

        hospital_Client.wsSend(ws_chat_data_model);
        return false;
    }

    public HttpCookieJar getCookieJar()
    {
        return hospital_Client.getCookieJar();
    }
}
