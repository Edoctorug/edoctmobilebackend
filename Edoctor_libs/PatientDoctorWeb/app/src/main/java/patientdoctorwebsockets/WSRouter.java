package patientdoctorwebsockets;

import java.util.Scanner;
import java.util.concurrent.atomic.AtomicBoolean;

import patientdoctorwebsockets.Models.ResponseModel;

public class WSRouter 
{
    AtomicBoolean found_online_doc = new AtomicBoolean();
    ResponseModel recent_response;
    public WSRouter()
    {
        found_online_doc.set(false);
    }
    public ResponseModel start()
    {
        while(found_online_doc.get()==false)
        {
        
        }
        found_online_doc.set(false);
        System.out.println("\n\tbegin message");
        return recent_response;
    }

    public void authHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }


    public void matchHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }

    public void msgHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }

    public void chatHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }

    public void appointmentsHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }

    public void appointmentHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }

    public void defaultHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }

    public void prescribeHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }

    public void prescriptionsHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }

    public void prescriptionHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }

    public void ordersHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }

    public void orderHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }

    public void recordsHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }

    public void recordHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }

    public void diagnosesHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }

    public void diagnosisHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }

    

    public void chatHistoryHandler(ResponseModel responseModel)
    {
        recent_response = responseModel;
    }
    public void route(ResponseModel response_model)
    {
        String status_type = response_model.status_type;
        int status_code = response_model.status_code;
        String status_msg = response_model.status_msg;
        System.out.println("\t\tAuth result: "+status_msg);
        switch(status_type)
        {
            case "auth":
                System.out.println("\t\tAuth result: "+status_msg);
                authHandler(response_model);
            break;

            case "match":
                found_online_doc.set(true);
                System.out.println("\t\tmatch result: "+status_msg);
                matchHandler(response_model);
            break;

            case "chat":
                found_online_doc.set(true);
                msgHandler(response_model);
                System.out.println("\t\t From message: "+status_msg);

            case "appointments":
                found_online_doc.set(true);
                appointmentsHandler(response_model);
                System.out.println("\t\t Appointment Message: "+status_msg);
            break;



            case "prescribe":
                found_online_doc.set(true);
                prescribeHandler(response_model);
                System.out.println("\t\t Appointment Message: "+status_msg);
            break;

            case "prescriptions":
                found_online_doc.set(true);
                prescriptionsHandler(response_model);
                System.out.println("\t\t Appointment Message: "+status_msg);
            break;

            case "chat_history":
                found_online_doc.set(true);
                chatHistoryHandler(response_model);
                System.out.println("\t\t Chat History Message: "+status_msg);
            break;

            case "records":
                found_online_doc.set(true);
                recordsHandler(response_model);
                System.out.println("\t\t records Message: "+status_msg);
            break;
            case "orders":
                found_online_doc.set(true);
                ordersHandler(response_model);
                System.out.println("\t\t orders Message: "+status_msg);
            break;
            case "order":
                found_online_doc.set(true);
                orderHandler(response_model);
                System.out.println("\t\t orders Message: "+status_msg);
            break;
            case "diagnoses":
                found_online_doc.set(true);
                diagnosesHandler(response_model);
                System.out.println("\t\t Appointment Message: "+status_msg);
            break;
            default:
                defaultHandler(response_model);
            break;
        }

    }


}
