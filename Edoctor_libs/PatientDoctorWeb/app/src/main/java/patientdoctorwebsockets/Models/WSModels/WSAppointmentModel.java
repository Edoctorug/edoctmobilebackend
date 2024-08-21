package patientdoctorwebsockets.Models.WSModels;

import patientdoctorwebsockets.Models.WSModels.WSMainModel;
import java.time.LocalTime;
public class WSAppointmentModel extends WSMainModel
{
    public long date;
    public long now_date;

    public String  now_time;
    public String time;

    public String note;
}