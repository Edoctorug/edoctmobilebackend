package patientdoctorwebsockets.Models.WSModels;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class WSChatMsgModel 
{
  public String cmd;
  public String message; //websoocket message
  public Object meta;   
  public String chat_uuid;
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
