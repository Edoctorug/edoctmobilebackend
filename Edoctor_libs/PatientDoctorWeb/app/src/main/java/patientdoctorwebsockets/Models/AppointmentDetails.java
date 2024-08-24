
package patientdoctorwebsockets.Models;

import java.util.LinkedHashMap;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;


/**
 * Represents the details of an appointment.
 */
public class AppointmentDetails 
{
    /**
    * The Appointment with doctor or patient
    */
    public String appointment_with = ""; //doctor or patient

    /**
    * The UUID of an appointment.
    */
    public String appointment_uuid = "";  //uuid of the appointment

    /**
    * Time the appointment will take place
    */
    public String appointment_time = ""; //time the appointment will take place

    /**
     * time the appointment was made
     */
    public String appointment_initial_time = ""; //time the appointment was made

    /**
     * date when the appointment will take place
     */
    public String appointment_date = ""; //date when the appointment will take place

    /**
     * date when the appointment was made
     */
    public String appointment_initial_date=""; //date when the appointment was made
    
    //LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd/MMM/yyyy HH:mm:ss a")); // get the current date and time when

    /**
    * additional note on the appointment
    */
    public String appointment_note = ""; //note on the appointment


    /**
     * Converts the AppointmentDetails object to a JSON string representation.
     *
     * @return The JSON string representation of the AppointmentDetails object.
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
     * Deserialize the given JSON string into an instance of AppointmentDetails.
     * 
     * @param json_String The JSON string to be deserialized.
     * @return An instance of AppointmentDetails if the deserialization is successful, otherwise null.
     */
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

    /**
     * Converts a LinkedHashMap object into an AppointmentDetails object by deserializing the JSON representation.
     * 
     * @param hashmap The LinkedHashMap object representing the JSON data.
     * @return The deserialized AppointmentDetails object.
     */
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
