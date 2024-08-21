package patientdoctorwebsockets.Models;

import java.util.LinkedHashMap;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import com.fasterxml.jackson.annotation.JsonCreator; 
import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * Class holding a chat message template
 * @property MEDIA_MSG constant for a nessage containing media. e.g an image, or video or sound recording value = 1998
 * @property TEXT_MSG constant for a nessage containing text only. value = 1999
 *@property message variable to hold the message.
 * @property is_patient boolean variable holding user type ( true for patient , false for doctor)
 * @property msg_type integer holding the message type
 *
 * @constructor
 * @param msg message to send
 * @param stat patient status true for patient , false for doctor
 * @param amsg_type type of message
 */
public class ChatModel
{
    public boolean msg_owner; //0 for mine 1 for another
    public boolean msg_type; //0 for text 1 for media message
    public String msg_data;
    public String msg_timestamp;
    
    @JsonCreator
    public ChatModel(@JsonProperty("msg_data") String data,@JsonProperty("msg_owner") boolean owner, @JsonProperty("msg_type")boolean type)
    {
        msg_owner = owner;
        msg_type = type;
        msg_data = data;
    }
    

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

    public static ChatModel deJson(String json_String)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
        ChatModel this_chat_detail = object_mapper.readValue(json_String,ChatModel.class); //deserialize json object into a java class
        
        return this_chat_detail; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }

    public static ChatModel deJson(LinkedHashMap hashmap)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
            ObjectMapper objectMapper = new ObjectMapper();
            String json_String = objectMapper.writeValueAsString(hashmap);
            ChatModel this_chat_detail = object_mapper.readValue(json_String,ChatModel.class); //deserialize json object into a java class
        
            return this_chat_detail; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }

}