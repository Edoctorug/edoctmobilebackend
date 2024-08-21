package patientdoctorwebsockets.Models;

import java.util.LinkedHashMap;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
public class ChatSummary
{

    public String chat_name;
    public String chat_time_date;
    

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

    public static ChatSummary deJson(String json_String)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
        ChatSummary this_chat_detail = object_mapper.readValue(json_String,ChatSummary.class); //deserialize json object into a java class
        
        return this_chat_detail; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }

    public static ChatSummary deJson(LinkedHashMap hashmap)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
            ObjectMapper objectMapper = new ObjectMapper();
            String json_String = objectMapper.writeValueAsString(hashmap);
            ChatSummary this_chat_detail = object_mapper.readValue(json_String,ChatSummary.class); //deserialize json object into a java class
        
            return this_chat_detail; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }

}