import requests
from exceptions import UpdateDataError,URLStatusCodeError,InvalidDataError,ContentTypeError,IdError


class BaseAPIData:
    """Base RJAPI class where there is written main methods to get and update data"""

    @staticmethod
    def _get_params(params: dict):
        """
        Checks whether there are any params
        If they do,returns them

        """

        pars = ""
        if params:
            for one in params:
                pars += f"/{params.get(one)}"
            return pars
        return pars

    def data(self,params=None) -> "json":
        """Returns serialized json data"""

        pars = self._get_params(params)
        if self.url != None:
            data = requests.get(self.url + pars)
        else:
            data = requests.get(self.get + pars)
        if data.status_code != 200:
            raise URLStatusCodeError
        return data.json()

    def update_data(self, json_data: dict,params: dict = None) -> None:
        """Updates data"""

        if self.url != None or self.put != None:
            if self.url != None and self.put != None:
                raise SettingsError
            
            pars = self._get_params(params)
            if self.url != None:
                if self.content_type == "json":
                    new_data = requests.put(self.url + pars, json=json_data)
                else:
                    raise ContentTypeError 
            else:
                if self.content_type == "json":
                    new_data = requests.put(self.put + pars, json=json_data)
                else:
                    raise ContentTypeError
            if new_data.status_code != 200:
                raise InvalidDataError
            return None 
            
        raise UpdateDataError


    def __repr__(self):
        return f"{self.__class__}"


    def __str__(self):
        if self.__class__.__doc__ != None:
            return f"Class - {self.__class__.__name__}\nDocString - {self.__class__.__doc__}"
        return f"Class - {self.__class__.__name__}"

class APIModifiedData(BaseAPIData):
    """
    This class is a main one beetween user and 'BaseClass'
    Here you can get data and update it 
    
    """

    def get_and_update_data(self,get_params=None,json_data=None):
        """
        It returns data and updates it using gotten id 
        and calling update_date method putting all the
        important parrams  

        """

        data = super().data(params=get_params)
        try:
            pks = [element["id"] for element in data]
            for index in pks:
                super().update_data(json_data=json_data,params={"pk":index})
            return data
        except KeyError:
            raise IdError
        


    def update_and_get_data(self,json_dict,get_params=None,put_params=None):
        """
        Firstly updates data using written 'put_params'
        and after calls data method to return json of new data
        PUD:
        It is better to write the same id of element you wanna get 
        to get an appropriate result.

        """

        super().update_data(json_data=json_dict,params=put_params)
        return super().data(get_params)



class APIDefaultSetting(APIModifiedData):
    """This class configures params for the futher work"""

    url = None
    get = None
    put = None
    delete = None
    post = None
    content_type = "json"

class RJAPI(APIDefaultSetting):
    """This one validates new-made params for 'APIDefaultSetting'"""

    def __init__(self):
        return self.save()

    @classmethod
    def save(cls):
        """Checks whether user's Meta class has these attributes to configure APISettings"""

        try:
            if hasattr(cls.Meta,"url"):
                cls.url = cls.Meta.url
            if hasattr(cls.Meta,"get"):
                cls.get = cls.Meta.get
            if hasattr(cls.Meta,"put"):
                cls.put = cls.Meta.put
            if hasattr(cls.Meta,"delete"):
                cls.delete = cls.Meta.delete
            if hasattr(cls.Meta,"post"):
                cls.post = cls.Meta.post
            if hasattr(cls.Meta,"content_type"):
                cls.content_type = cls.Meta.content_type
        except AttributeError:
            raise AttributeError("You haven't passed Meta class or written wrong attributes")
