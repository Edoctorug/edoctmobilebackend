import json

class WSResponseMdl:
    """
    Model for WebSocket response.

    Attributes:
        status_code (int): The status code of the response.
        status_type (str): The type of status.
        status_msg (str): The status message.
        meta_data (dict): Additional metadata associated with the response.
    """
    status_code = 200
    status_type = ""
    status_msg = ""
    meta_data = {}

    def __init__(self,code,type,msg,meta={}):
        """
        Initializes a WebSocket response model.

        Args:
            code (int): The status code of the response.
            type (str): The type of status.
            msg (str): The status message.
            meta (dict, optional): Additional metadata associated with the response. Default is an empty dictionary.
        """
        self.status_code = code
        self.status_msg = msg
        self.meta_data = meta
        self.status_type = type
    
    def serial(self):
        """
        Serializes the WebSocket response model into JSON format.

        Returns:
            str: JSON representation of the response model.
        """
        json_data = json.dumps(self.__dict__)
        return str(json_data)
        