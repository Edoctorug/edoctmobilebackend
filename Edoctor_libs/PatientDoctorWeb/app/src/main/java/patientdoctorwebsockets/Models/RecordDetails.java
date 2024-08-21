package patientdoctorwebsockets.Models;

import java.util.LinkedHashMap;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
public class RecordDetails 
{
    public String record_title;
    public String record_for;
    public String record_author;
    public String record_uuid;
    public String record_time = LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd/MMM/yyyy HH:mm:ss a")); // get the current date and time when
    public String record_date;
    public String record_details;
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

    public static RecordDetails deJson(String json_String)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
        RecordDetails this_chat_detail = object_mapper.readValue(json_String,RecordDetails.class); //deserialize json object into a java class
        
        return this_chat_detail; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }

    public static RecordDetails deJson(LinkedHashMap hashmap)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
            ObjectMapper objectMapper = new ObjectMapper();
            String json_String = objectMapper.writeValueAsString(hashmap);
            RecordDetails this_chat_detail = object_mapper.readValue(json_String,RecordDetails.class); //deserialize json object into a java class
        
            return this_chat_detail; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }
    
}
