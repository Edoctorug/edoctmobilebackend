package patientdoctorwebsockets.Models.WSModels;


import patientdoctorwebsockets.Models.WSModels.WSMainModel;

public class WSOrderModel extends WSMainModel
{
    public String item_name;
    public int item_quantity;
    public String pharmacy_id;

    public WSOrderModel(String xitem_name,int xitem_quantity,String xpharmacy_id)
    {
        item_name = xitem_name;
        item_quantity = xitem_quantity;
        pharmacy_id = xpharmacy_id;

    }
}