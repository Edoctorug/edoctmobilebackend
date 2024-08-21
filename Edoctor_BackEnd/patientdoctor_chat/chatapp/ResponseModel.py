import json

class ResponseMdl:
    '''
    Blueprint for a response 
    Attributes:
      status_code - status code for the json response 
      status_msg - message to include in the json response
      meta_data - any extra data to include in the status response
    '''
    
    '''
    status code variable
    '''
    status_code = 200 #status code for the json response
    status_msg = ""
    meta_data = {}

    def __init__(self,code,msg,meta={}):
        '''
        Constructor
        
        Parameters:
          code - status code to use
          msg - message in the json response
          meta - any extra data to add to the response
        '''
        self.status_code = code
        self.status_msg = msg
        self.meta_data = meta
    
    def serial(self):
        '''
        Converts this object data to a json string
        
        returns json string
        '''
        json_data = json.dumps(self.__dict__)
        return str(json_data)
        