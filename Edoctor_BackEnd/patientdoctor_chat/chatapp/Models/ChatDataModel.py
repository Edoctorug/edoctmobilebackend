from .MainModel import *
class ChatDataModel(MainModel):
    """A class for storing and manipulating chat data.

    This class is used to store and manipulate chat data in a structured way.
    It contains the following attributes:

    Attributes:
       to_name: The name of the recipient of the chat message.
       to_type: The type of the recipient of the chat message.
       from_name: The name of the sender of the chat message.
       from_type: The type of the sender of the chat message.
       data: The actual chat message data.
    Args:
       xto_name: The name of the recipient of the chat message.
       xto_type: The type of the recipient of the chat message.
       xfrom_name: The name of the sender of the chat message.
       xfrom_type: The type of the sender of the chat message.
       data: The actual chat message data.
       data_type: The data type of the message data
    """
    
    def __init__(self,xsender_name,xsender_type,xrecv_name,xrecv_type,xdata,xdata_type,xchat_time):
        self.sender_name = xsender_name
        self.sender_role = xsender_type
        self.recv_name = xrecv_name
        self.recv_type = xrecv_type
        self.data = xdata
        self.data_type = xdata_type
        self.chat_time = xchat_time
