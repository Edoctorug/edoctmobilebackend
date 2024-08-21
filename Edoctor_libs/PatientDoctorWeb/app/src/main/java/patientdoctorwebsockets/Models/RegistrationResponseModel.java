package patientdoctorwebsockets.Models;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.JsonProcessingException;
import patientdoctorwebsockets.Models.UserDetails;

public class RegistrationResponseModel extends UserDetails //class Registration to store the registration details from the server
{
    public boolean deJson(String json_String)
    {
        ObjectMapper object_mapper = new ObjectMapper();

        try
        {
        object_mapper.readValue(json_String,this.getClass());

        return true;
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return false;
    }
}
