package patientdoctorwebsockets.Models;

import java.util.LinkedHashMap;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import patientdoctorwebsockets.Models.*;

/**
 * Represents the appointments History
 */
public class AppointmentsHistory
{
    
    /**
     * <b>The appointments history</b>
     * An array of the {@link patientdoctorwebsockets.Models.AppointmentDetails} objects
     */
    public AppointmentDetails[] appointments_history ;
    
    /**
     * Converts the object to a JSON string representation.
     *
     * @return The JSON string representation of the object.
     */
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

    /**
     * Deserialize the given JSON string into an instance of the AppointmentsHistory class.
     * 
     * @param json_String The JSON string to be deserialized.
     * @return An instance of the AppointmentsHistory class if the deserialization is successful, otherwise null.
     */
    public static AppointmentsHistory deJson(String json_String)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
        AppointmentsHistory this_appointment_detail = object_mapper.readValue(json_String,AppointmentsHistory.class); //deserialize json object into a java class
        
        return this_appointment_detail; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }

    /**
     * Converts a LinkedHashMap object into an instance of the AppointmentsHistory class.
     * 
     * @param hashmap The LinkedHashMap object to be converted.
     * @return An instance of the AppointmentsHistory class if the conversion is successful, otherwise null.
     */
    public static AppointmentsHistory deJson(LinkedHashMap hashmap)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
            ObjectMapper objectMapper = new ObjectMapper();
            String json_String = objectMapper.writeValueAsString(hashmap);
            AppointmentsHistory this_appointment_detail = object_mapper.readValue(json_String,AppointmentsHistory.class); //deserialize json object into a java class
        
            return this_appointment_detail; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }
    
}
