package patientdoctorwebsockets;


import okhttp3.*;
import patientdoctorwebsockets.Models.ResponseModel;
import patientdoctorwebsockets.Models.ChatDetails;
public class WSmanCB extends WebSocketListener //Websocket listener
{
    WSRouter ws_router;// = new WSRouter();;

    public WSRouter getActiveRouter()
    {
        return ws_router;
    }

    public WSRouter setActiveRouter(WSRouter ws_routerx)
    {
        ws_router = ws_routerx;

        return ws_router;
    }

    @Override
    public void onOpen(WebSocket webSocket, Response response) //after successful connection
    {
        // TODO Auto-generated method stub
        super.onOpen(webSocket, response);
        
        System.out.println("\t\t\t--Connection Successful\n");
        
    }

    @Override
    public void onMessage(WebSocket webSocket, String text) //after getting message
    {
        // TODO Auto-generated method stub
        super.onMessage(webSocket, text);
        System.out.println("\nreply data: "+text);
        ResponseModel responseModel = ResponseModel.deJson(text);
        System.out.println("Reply: "+text);
        
        System.out.println("\nMeta Reply: ");
        
        ws_router.route(responseModel);
        
        
    }

    @Override
    public void onFailure(WebSocket webSocket, Throwable t, Response response) //websocket failed
    {
        // TODO Auto-generated method stub
        super.onFailure(webSocket, t, response);
        
        System.out.println("\t\tSocket failed: "+t.getMessage());
    }

    @Override
    public void onClosed(WebSocket webSocket, int code, String reason) //websocket has closed
    {
        // TODO Auto-generated method stub
        super.onClosed(webSocket, code, reason);
        System.out.println("\t\tSocket closed\n");
    }

    @Override
    public void onClosing(WebSocket webSocket, int code, String reason) //websocket connection is closing
    {
        // TODO Auto-generated method stub
        super.onClosing(webSocket, code, reason);
        System.out.println("\t\tsocket closing\n");
    }


}
