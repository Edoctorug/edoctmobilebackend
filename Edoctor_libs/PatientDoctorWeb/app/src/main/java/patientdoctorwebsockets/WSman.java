package patientdoctorwebsockets;

import okhttp3.WebSocket;
import okhttp3.WebSocketListener;
import okhttp3.OkHttpClient;
import okhttp3.Request;

public class WSman
{
    String ws_url = "";
    String ws_addr = ""; //websocket address
    int ws_port; //websocket server port
    WebSocket web_socket;
    OkHttpClient parent_httpclient;
    WebSocketListener webSocketListener;
    public WSman(OkHttpClient okHttpClient,String aws_addr,int aws_port,String path_to_websocket,WebSocketListener xwebSocketListener)//constructor argument is a websocket address
    {
        
         
        ws_port = aws_port;
        webSocketListener = xwebSocketListener;
        if(aws_addr.contains("http")){
            ws_addr = aws_addr.replace("http","ws");
        }
        else if(aws_addr.contains("https")){
            ws_addr = aws_addr.replace("https","wss");
        }
        else{
            ws_addr = aws_addr;
        }

        if(aws_port>0)
        {
            if(ws_addr.contains("ws") || ws_addr.contains("wss"))
            {
                ws_url = ws_addr+":"+ws_port; // build websocket url
            }
            else{
                ws_url = "ws://"+ws_addr+":"+ws_port; // build websocket url
            }
        }
        else
        {
            if(ws_addr.contains("ws") || ws_addr.contains("wss"))
            {
                ws_url = ws_addr;
            }
            else{
                ws_url = "ws://"+ws_addr;
            }
        }
        parent_httpclient = okHttpClient;
        /*Request request = new Request.Builder()
        .url(ws_addr)
        .build();
        web_socket = okHttpClient.newWebSocket(request, new WSmanCB());*/
 //websocket request builder
        String full_path = ws_url+path_to_websocket;
        System.out.println("\nwebsocket endpoint: "+full_path);
        Request request = new Request.Builder()
        .url(full_path)
        .build();
 
        web_socket = parent_httpclient.newWebSocket(request, webSocketListener);
    }

    public boolean sendData(String data_to_send) //method to send data over websockets
    {
        
        System.out.println(data_to_send);
        return web_socket.send(data_to_send);
        
    }

    public boolean stop()
    {
        web_socket.cancel();
        return true;
    }

    



}