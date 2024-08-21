package patientdoctorwebsockets;

import okhttp3.*;
import java.util.ArrayList;
import java.util.List;

public class HttpCookieJar implements CookieJar {
    private List<Cookie> cookies;

    @Override
    public void saveFromResponse(HttpUrl url, List<Cookie> cookies) {
        this.cookies =  cookies;
    }

    @Override
    public List<Cookie> loadForRequest(HttpUrl url) {
        if (cookies != null)
            return cookies;
        return new ArrayList<Cookie>();

    }
}