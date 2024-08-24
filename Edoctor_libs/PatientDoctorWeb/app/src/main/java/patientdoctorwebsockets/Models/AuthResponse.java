package patientdoctorwebsockets.Models;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.JsonProcessingException;
import patientdoctorwebsockets.Models.UserDetails;

/**
 * Represents the authentication response from the server.
 */
public class AuthResponse //class Registration to store the registration details from the server
{   
    /**
     * status code
     */
    public int status_code;

    /**
     * status message
     */
    public String status_msg;

    /**
     * user details {@link patientdoctorwebsockets.Models.UserDetailsCompact}
     */
    public UserDetailsCompact meta_data;


    /**
     * Deserialize the given JSON string into an instance of AuthResponse.
     * 
     * @param json_String The JSON string to be deserialized.
     * @return An instance of AuthResponse if the deserialization is successful, otherwise null.
     */
    
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
