package patientdoctorwebsockets.Models;

import java.util.LinkedHashMap;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
public class ItemDetails 
{
    public String item_name;
    public String item_sku;
    public String item_price;
    public String item_description;
    public String item_pic_url;

    
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

    public static ItemDetails deJson(String json_String)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
        ItemDetails this_chat_detail = object_mapper.readValue(json_String,ItemDetails.class); //deserialize json object into a java class
        
        return this_chat_detail; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }

    public static ItemDetails deJson(LinkedHashMap hashmap)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
            ObjectMapper objectMapper = new ObjectMapper();
            String json_String = objectMapper.writeValueAsString(hashmap);
            ItemDetails this_chat_detail = object_mapper.readValue(json_String,ItemDetails.class); //deserialize json object into a java class
        
            return this_chat_detail; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }
    
}
