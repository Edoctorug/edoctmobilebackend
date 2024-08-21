package patientdoctorwebsockets.Models;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class AuthModel {
    public String user_name;
    public String user_password;

    public AuthModel(String uname, String upass)//auth model constructor with user name(uname) and user password(upass)
    {
        user_name = uname;
        user_password = upass;
    }
    public String toJson() //serialize this module to json
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