package patientdoctorwebsockets.Models;

import java.util.LinkedHashMap;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import com.fasterxml.jackson.annotation.JsonCreator; 
import com.fasterxml.jackson.annotation.JsonProperty;



/**
 * Represents a chat message in the application.
 * 
 * This class provides methods to convert the chat message to JSON format and deserialize JSON into a ChatModel object.
 * 
 * @version 1
 * @author aivan2798
 * @since [current date]
 */

public class ChatModel
{
    public boolean msg_owner; //0 for mine 1 for another
    public boolean msg_type; //0 for text 1 for media message
    public String msg_data;
    public String msg_timestamp;
    


    /**
     * Constructs a new ChatModel object.
     *
     * @param data   the message data
     * @param owner  the message owner true for patient, false for doctor
     * @param type   the message type: <p>can be MEDIA_MSG constant for a nessage containing media. e.g an image, or video or sound recording value = 1998</p> or <p>TEXT_MSG constant for a nessage containing text only. value = 1999</p>
     * 
     */
    @JsonCreator
    public ChatModel(@JsonProperty("msg_data") String data,@JsonProperty("msg_owner") boolean owner, @JsonProperty("msg_type")boolean type)
    {
        msg_owner = owner;
        msg_type = type;
        msg_data = data;
    }
    
    /**
    * Converts the ChatModel object to a JSON string.
    *
    * @return String the JSON representation of the ChatModel object
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
     * Deserialize the given JSON string into a ChatModel object.
     *
     * @param json_String The JSON string to be deserialized.
     * @return The ChatModel object deserialized from the JSON string, or null if unsuccessful.
     */
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


    /**
     * Deserialize a JSON object into a ChatModel instance.
     *
     * @param hashmap The LinkedHashMap representing the JSON object to be deserialized.
     * @return The deserialized ChatModel instance if successful, otherwise null.
     */
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