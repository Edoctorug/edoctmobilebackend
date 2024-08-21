package patientdoctorwebsockets.Models;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class ResponseModel {
    public int status_code = 200;
    public String status_type = "";
    public String status_msg = "";
    public Object meta_data;

    public static ResponseModel deJson(String json_String)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
        ResponseModel this_auth_response = object_mapper.readValue(json_String,ResponseModel.class); //deserialize json object into a java class
        
        return this_auth_response; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }
}
