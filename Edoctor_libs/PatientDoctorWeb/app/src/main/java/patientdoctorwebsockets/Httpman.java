package patientdoctorwebsockets;



import java.io.IOException;
import java.net.CookieManager;
import java.util.List;
import okhttp3.*;
import patientdoctorwebsockets.HttpCookieJar;
//import okhttp3.JavaNetCookieJar;
public class Httpman {
    OkHttpClient okhttpclient;
    HttpCookieJar http_CookieJar;
    public MediaType JSON = MediaType.parse("application/json; charset=utf-8");
    String http_url;
    String base_url;
    int http_port;
    WSman http_wsman;
    String cookie_value = "";
    public Httpman(String url,int port)//contructor with endpoint url and port number
    {
        http_url = url;
        http_port = port;
        base_url = http_url;
        http_CookieJar = new HttpCookieJar();

        okhttpclient = new OkHttpClient.Builder()
                .cookieJar(http_CookieJar)
                .build();
        
    }

    public String send(String data,String path)
    {
        
        String send_http_url = "";
        if(http_port>0) //check if port is specified
        {
            send_http_url = "http://"+http_url+":"+http_port+path;
        }
        else
        {
            send_http_url = "http://"+http_url+path;
        } //build url for server
        System.out.println("sending to http server: "+send_http_url);
        RequestBody request_body = RequestBody.create(JSON,data);
        Request arequest = new Request.Builder().url(send_http_url).post(request_body).build();

        
        try
        {
           Response http_response = okhttpclient.newCall(arequest).execute();
           String response_str = http_response.body().string();
           //System.out.println(response_str);

           
           return response_str;
        }
        catch(IOException ioe)
        {
            System.out.println(ioe.getMessage());
            
        }

        return null;

    }

    public void initWebSocket(String wspath,WebSocketListener web_socket_listener)//method to initialize the websocket server to the web socket path wspath
    {
        http_wsman = new WSman(okhttpclient, base_url, http_port,wspath,web_socket_listener);
        
    }

    public boolean wsSend(String wsdata)//function send data (wsdata) to web socket path(wspath)
    {
    
        return http_wsman.sendData(wsdata);
    }

    public boolean wsStop()//stop websocket connection
    {
        return http_wsman.stop();
    }

    public String getCookie(String cookie_name) //return cookie value from cookie with cookie_name
    {
        List<Cookie> my_cookies = http_CookieJar.loadForRequest(HttpUrl.parse(http_url));

        String temp_cookie_value = "";
           for(Cookie acookie:my_cookies)
           {
            String temp_cookie_name = acookie.name(); //get cookie name
            temp_cookie_value = acookie.value();//get cookie value
            System.out.println("Cookie Value: "+temp_cookie_value+" cookie name: "+temp_cookie_name);
            if(temp_cookie_name.equals(cookie_name))
            {
                //System.out.println("\nsame same");
                temp_cookie_value = acookie.value();
                //return acookie.value();
                
            }
             //get cookie value temporarily
            
           }
        return temp_cookie_value;
    }

    public HttpCookieJar getCookieJar()
    {
        return http_CookieJar;
    }
}
