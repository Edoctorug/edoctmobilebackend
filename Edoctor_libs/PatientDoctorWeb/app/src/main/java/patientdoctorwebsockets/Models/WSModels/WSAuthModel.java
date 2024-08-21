package patientdoctorwebsockets.Models.WSModels;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;


public class WSAuthModel //model representing data to be sent to the websocket auth endpoint
{
    public String cmd; //websocket server command 
    public String message; //websoocket message
    public Object meta;

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
