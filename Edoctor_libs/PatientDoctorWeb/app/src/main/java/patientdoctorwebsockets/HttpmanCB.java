package patientdoctorwebsockets;

import okhttp3.*;
import java.io.IOException;
public class HttpmanCB implements Callback {

    @Override
    public void onResponse(Call call, Response response) {
        // Handle successful response here
        try
        {
        if (response.isSuccessful()) {
            // Process the response body
            ResponseBody responseBody = response.body();
            if (responseBody != null) {
                // Read the response data
                String responseData = responseBody.string();
                System.out.println("Response data: " + responseData);
            }
        } else {
            // Handle non-successful response (e.g., 404, 500, etc.)
            System.err.println("Error: " + response.code() + " - " + response.message());
        }
    }
    catch(IOException ioe)
    {
        System.out.println(ioe.getMessage());
    }
    }

    @Override
    public void onFailure(Call call, IOException e) {
        // Handle request failure (e.g., network issues, timeouts, etc.)
        System.err.println("Request failed: " + e.getMessage());
    }
}
