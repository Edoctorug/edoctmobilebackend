package patientdoctorwebsockets.Models.WSModels;


import patientdoctorwebsockets.Models.WSModels.WSMainModel;
import java.time.Instant;
import java.time.LocalTime;
import java.time.LocalDate;

public class WSPatientRecordModel extends WSMainModel
{
    public String record_title;
    public String record_details;

    public String record_date;
    public String record_time;
    public long record_timestamp;

    public WSPatientRecordModel(String xrecord_title,String xrecord_details)
    {
        record_title = xrecord_title;
        
        record_details = xrecord_details;

        record_date = LocalDate.now().toString();

        record_time = LocalTime.now().toString();

        record_timestamp = Instant.now().toEpochMilli();
    }
}