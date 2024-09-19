
from .models import *
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async



#class to get user details
class UserDB:
    def __init__(self):
        pass

    async def getFullNames(self,userID):
        """
        Retrieves the full names associated with the given user ID asynchronously.

        Args:
            self: The instance of the class.
            userID (int): The user ID for which full names are to be retrieved.

        Returns:
            str: The full names associated with the given user ID.
        """
        get_full_names = sync_to_async(self.getFullnames)
        user_names = await get_full_names(userID)
        return user_names
    
    async def getUserObject(self,userID):
        """
        Retrieves the full names associated with the given user ID asynchronously.

        Args:
            self: The instance of the class.
            userID (int): The user ID for which full names are to be retrieved.

        Returns:
            str: The full names associated with the given user ID.
        """
        get_user_object = sync_to_async(self.getUserobject)
        user_object = await get_user_object(userID)

        return user_object
    
    def getUserobject(self,userID):
        """
        Retrieves the user object associated with the given user ID.

        Args:
            self: The instance of the class.
            userID (int): The user ID for which full names are to be retrieved.

        Returns:
            User: User object associated with the given user ID.
        """
        hospital_user = User.objects.get(id = userID)
        print("internal : ", hospital_user)
        return  hospital_user
    def getFullnames(self,userID):
        """
        Retrieves the full names associated with the given user ID.

        Args:
            self: The instance of the class.
            userID (int): The user ID for which full names are to be retrieved.

        Returns:
            str: The full names associated with the given user ID.
        """
        hospital_user = User.objects.get(id = userID)
        print("internal : ", hospital_user)
        return  hospital_user.get_full_name()

    async def getUserObjectFromUserName(self,user_name):
        get_user_object = sync_to_async(self.getUserObjectFromusername)
        user_object = await get_user_object(user_name)
        return user_object

    def getUserObjectFromusername(self,user_name):
        """
        Retrieves the full names associated with the given user ID.

        Args:
            self: The instance of the class.
            userID (int): The user ID for which full names are to be retrieved.

        Returns:
            str: The full names associated with the given user ID.
        """
        hospital_user = User.objects.get(username = user_name)
        print("internal : ", hospital_user)
        return  hospital_user
    
    async def getPatientObject(self,userID):
        """
            Retrieves the patient object associated with the given user ID asynchronously.

        Args:
            self: The instance of the class.
            userID (int): The user ID for which the patient object is to be retrieved.

        Returns:
            Patients: The patient object associated with the given user ID.
        """
        get_patient = sync_to_async(lambda auserID:Patients.objects.get(user_id = auserID))
        return await get_patient(userID)
    
    async def getDoctorObject(self, userID):
        """
        Retrieves the doctor object associated with the given user ID asynchronously.

        Args:
            self: The instance of the class.
            userID (int): The user ID for which the doctor object is to be retrieved.

        Returns:
            Doctors: The doctor object associated with the given user ID.
        """
        get_doctor = sync_to_async(lambda auserID:Doctors.objects.get(user_id = auserID))
        return await get_doctor(userID)
    
    async def getChatObject(self, userID):
        """
        Retrieves the chat object associated with the given user ID asynchronously.

        Args:
            self: The instance of the class.
            userID (int): The user ID for which the chat object is to be retrieved.

        Returns:
            Chats: The chat object associated with the given user ID.
        """
        get_chat = sync_to_async(lambda auserID:Chats.objects.get(sender = auserID))
        return await get_chat(userID)
    
    async def getChannelName(self, userID):
        """
            Retrieves the channel name associated with the given user ID asynchronously.

        Args:
            self: The instance of the class.
            userID (int): The user ID for which the channel name is to be retrieved.

        Returns:
            str: The channel name associated with the given user ID.
        """
        get_channel_name = (sync_to_async( lambda auserID:HospitalUsers.objects.get(user_id = auserID).channel_name)) #async version to get the user's channel name using userID

        return await get_channel_name(userID)
    
    async def getHospitalObject(self, userID):
        """
        Retrieves the hospital object associated with the given user ID asynchronously.

        Args:
            self: The instance of the class.
            userID (int): The user ID for which the hospital object is to be retrieved.

        Returns:
            HospitalUsers: The hospital object associated with the given user ID.
        """
        print("\t\tfinding hoapital user: ",userID)
        get_hospital_user = sync_to_async(lambda auserID:HospitalUsers.objects.get(user_id = auserID))
        return await get_hospital_user(userID)