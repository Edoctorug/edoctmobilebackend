from .MainModel import *
from time import time
class ChatMsgModel(MainModel):
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
    
    def __init__(self,msg_owner,msg_data,msg_type):
        self.msg_owner = msg_owner
        self.msg_data = msg_data
        self.msg_type = msg_type
        self.msg_timestamp = int(time())
