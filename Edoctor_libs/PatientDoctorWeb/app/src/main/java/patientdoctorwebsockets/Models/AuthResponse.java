package patientdoctorwebsockets.Models;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.JsonProcessingException;
import patientdoctorwebsockets.Models.UserDetails;

public class AuthResponse //class Registration to store the registration details from the server
{
    public int status_code;
    public String status_msg;
    public UserDetailsCompact meta_data;
    public static AuthResponse deJson(String json_String)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
        AuthResponse this_auth_response = object_mapper.readValue(json_String,AuthResponse.class); //deserialize json object into a java class
        
        return this_auth_response; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }
}
