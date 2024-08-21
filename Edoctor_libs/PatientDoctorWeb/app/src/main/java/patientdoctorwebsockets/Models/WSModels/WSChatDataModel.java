package patientdoctorwebsockets.Models.WSModels;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.Instant;
import java.time.LocalTime;
import java.time.LocalDate;

public class WSChatDataModel {
    public String cmd; //websocket server command 
    public String message; //websocket message
    public String meta = "";
    public String chat_uuid = "";
    public long chat_time;

    public WSChatDataModel()
    {
        chat_time = Instant.now().toEpochMilli();
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
}
