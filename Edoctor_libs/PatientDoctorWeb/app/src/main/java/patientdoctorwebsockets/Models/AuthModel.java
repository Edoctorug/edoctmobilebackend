
package patientdoctorwebsockets.Models;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Represents an authentication model used to hold user credentials i.e username and password.
 */
public class AuthModel {

    /**
     * username
     */
    public String user_name;

    /**
     * hospital password
     */
    public String user_password;

    /**
     * Represents an authentication model for a user.
     * 
     * @param uname The user name.
     * @param upass The user password.
     */
    public AuthModel(String uname, String upass)//auth model constructor with user name(uname) and user password(upass)
    {
        user_name = uname;
        user_password = upass;
    }
    
    /**
     * Serializes the AuthModel object to JSON.
     *
     * @return The JSON representation of the AuthModel object.
     */
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