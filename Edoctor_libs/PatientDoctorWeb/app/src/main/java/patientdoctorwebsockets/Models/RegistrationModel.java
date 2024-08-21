package patientdoctorwebsockets.Models;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import com.fasterxml.jackson.core.JsonProcessingException;
import patientdoctorwebsockets.Models.UserDetails;

public class RegistrationModel extends UserDetails //Registration Model Class inheriting properties of the UserDetails class
{
    /*public String user_name;
    public String first_name;
    public String last_name;
    public String user_role;*/
    public String user_password;

    public String toJson()
    {
        ObjectMapper this_mapper = new ObjectMapper();
        String json_str = "";
        try
        {
           json_str = this_mapper.writeValueAsString(this);
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return json_str;
    }
}
