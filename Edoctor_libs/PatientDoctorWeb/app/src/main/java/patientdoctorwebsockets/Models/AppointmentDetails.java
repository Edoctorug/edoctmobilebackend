package patientdoctorwebsockets.Models;

import java.util.LinkedHashMap;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
public class AppointmentDetails 
{
    public String appointment_with = "";
    public String appointment_uuid = "";
    public String appointment_time = "";
    public String appointment_initial_time = "";
    public String appointment_date = "";
    public String appointment_initial_date="";
    
    //LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd/MMM/yyyy HH:mm:ss a")); // get the current date and time when
    public String appointment_note = "";
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

    public static AppointmentDetails deJson(String json_String)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
        AppointmentDetails this_chat_detail = object_mapper.readValue(json_String,AppointmentDetails.class); //deserialize json object into a java class
        
        return this_chat_detail; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }

    public static AppointmentDetails deJson(LinkedHashMap hashmap)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
            ObjectMapper objectMapper = new ObjectMapper();
            String json_String = objectMapper.writeValueAsString(hashmap);
            AppointmentDetails this_chat_detail = object_mapper.readValue(json_String,AppointmentDetails.class); //deserialize json object into a java class
        
            return this_chat_detail; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }
    
}
