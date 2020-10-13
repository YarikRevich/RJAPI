import requests
import asyncio
from .exception import UpdateDataError,URLStatusCodeError,InvalidDataError,ContentTypeError,IdError,HttpMethodError
from .utils import Utils
from .core import BaseAPIData


class APIModifiedData(BaseAPIData):
    """
    This class is a main one beetween user and 'BaseClass'
    Here you can get data and update it

    """

    async def get_data(self, get_params:dict = None, filters: dict =None) -> dict:
        """Returns the result of GET method without pk"""

        return await super().get_data(params=get_params,filters=filters)


    async def update_data(self, json_data: dict = None, params: dict = None, filters: dict = None, files: dict = None) -> dict:
        """
        Firstly updates data using written 'put_params'
        and after calls data method to return json of new data
        PUD:
        It is better to write the same id of element you wanna get
        to get an appropriate result.

        """

        await super().update_data(json_data=json_data,params=params,filters=filters,patch_req=True, files=files)
        return await super().get_data(params=params,filters=filters)


    async def create_entry(self, data:dict = None, files:dict = None) -> bool:
        """Method for the creating a new entry"""

        return await super().create_data(data=data, files=files)


    async def get_and_update_json(self,get_params: dict = None,json_data: dict = None, filters: dict = None,put_method:bool = False, patch_method:bool = False) -> dict:
        """
        It returns data and updates it using gotten id
        and calling update_date method putting all the
        important parrams

        """

        data = await super().get_data(params=get_params,filters=filters)
        try:
            try:
                pks = [element["id"] for element in data["results"]]
            except TypeError:
                pks = [element["id"] for element in data]
            for index in pks:
                if put_method:
                    await super().update_data(json_data=json_data,params={"pk":index},filters=filters,put_req=True)
                else:
                    await super().update_data(json_data=json_data,params={"pk":index},filters=filters,patch_req=True)
            return data
        except KeyError:
            raise IdError


class APIDefaultSetting(APIModifiedData):
    """This class configures params for the futher work"""

    url = None
    get = None
    put = None
    delete = None
    post = None
    auth_data = None
    content_type = "json"
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'


class RJAPI(APIDefaultSetting):
    """This one validates new-made params for 'APIDefaultSetting'"""

    def __init__(self):
        return self.save()

    @classmethod
    def save(cls) -> None:
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
            if hasattr(cls.Meta,"auth_data"):
                cls.auth_data = cls.Meta.auth_data
        except AttributeError:
            raise AttributeError("You haven't passed Meta class or written wrong attributes")
