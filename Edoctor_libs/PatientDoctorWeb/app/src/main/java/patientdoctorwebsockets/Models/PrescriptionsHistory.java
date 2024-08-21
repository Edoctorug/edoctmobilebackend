package patientdoctorwebsockets.Models;

import java.util.LinkedHashMap;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import patientdoctorwebsockets.Models.*;
public class PrescriptionsHistory
{
    
    
    public PrescriptionDetails[] prescriptions_history ;
    
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

    public static PrescriptionsHistory deJson(String json_String)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
        PrescriptionsHistory this_record_detail = object_mapper.readValue(json_String,PrescriptionsHistory.class); //deserialize json object into a java class
        
        return this_record_detail; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }

    public static PrescriptionsHistory deJson(LinkedHashMap hashmap)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
            ObjectMapper objectMapper = new ObjectMapper();
            String json_String = objectMapper.writeValueAsString(hashmap);
            PrescriptionsHistory this_record_detail = object_mapper.readValue(json_String,PrescriptionsHistory.class); //deserialize json object into a java class
        
            return this_record_detail; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }
    
}
