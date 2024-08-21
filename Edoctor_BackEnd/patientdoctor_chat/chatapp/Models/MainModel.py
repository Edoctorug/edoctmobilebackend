import json
class MainModel:
    def serial(self):
        """
        Serializes the object into JSON format.

        Returns:
            str: JSON representation of the object.
        """
        json_data = json.dumps(self.__dict__)
        return str(json_data)