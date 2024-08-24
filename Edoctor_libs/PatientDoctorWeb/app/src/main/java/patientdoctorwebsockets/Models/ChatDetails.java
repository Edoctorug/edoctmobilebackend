package patientdoctorwebsockets.Models;

import java.util.LinkedHashMap;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Represents the details about the user's chat.
 */
public class ChatDetails 
{
    /**
     * full names of the user being chatted with.
     */
    public String full_names;

    /**
     * full names of the person the doctor has been assigned to, only if the current user is not a patient.
     */
    public String assigned_patient;

    /**
     * the user's chat uuid representing the end users websocket to where the messages with be delivered.
     */
    public String chat_uuid;

    /**
     * the time the chat was recieved
     */

    public String chat_time = LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd/MMM/yyyy HH:mm:ss a")); // get the current date and time when


    /**
     * Converts the ChatDetails object to a JSON string representation.
     *
     * @return The JSON string representation of the ChatDetails object.
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
     * Deserialize the given JSON string into a ChatDetails object.
     * 
     * @param json_String The JSON string to be deserialized.
     * @return The ChatDetails object deserialized from the JSON string, or null if unsuccessful.
     */
    public static ChatDetails deJson(String json_String)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
        ChatDetails this_chat_detail = object_mapper.readValue(json_String,ChatDetails.class); //deserialize json object into a java class
        
        return this_chat_detail; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }

    /**
     * Converts a LinkedHashMap object into a ChatDetails object by deserializing the JSON representation.
     * 
     * @param hashmap The LinkedHashMap object representing the JSON data.
     * @return The ChatDetails object created from the JSON data, or null if the deserialization fails.
     */
    public static ChatDetails deJson(LinkedHashMap hashmap)
    {
        
        ObjectMapper object_mapper = new ObjectMapper(); //get jackson object mapper

        try
        {
            ObjectMapper objectMapper = new ObjectMapper();
            String json_String = objectMapper.writeValueAsString(hashmap);
            ChatDetails this_chat_detail = object_mapper.readValue(json_String,ChatDetails.class); //deserialize json object into a java class
        
            return this_chat_detail; //return true if successful
        }
        catch(JsonProcessingException jse)
        {
            System.out.println(jse.getMessage());
        }
        return null; //return false if unsuccessful
    }
    
}
