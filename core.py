import requests
from .utils import Utils
from .exception import (UpdateDataError,
                        URLStatusCodeError,
                        SettingsError,
                        ContentTypeError,
                        InvalidDataError,
                        HttpMethodError)


class BaseAPIData(Utils):
    """Base RJAPI class. Takes
    -> Update method
    -> Get method
    -> Create method

    """

    def get_data(self,params: dict = None,filters: dict = None) -> dict:
        """Returns the list of gotten data.Can take such params as:
        -> params (to get an equal entry)
        -> filters (to filter an important entry)
        """

        if self.url != None and self.get != None:
            raise SettingsError

        pars = self._get_params(params, filters)
        data = self._GET_request(params=pars)
        if data.status_code != 200:
            raise URLStatusCodeError
        return data.json()


    def update_data(self, json_data: dict,params: dict = None, filters:dict = None, files:dict = None,put_req: bool = False, patch_req: bool = False) -> None:
        """Updates data.Can take such params as:
        -> json-data
        -> params (to get an equal entry to update)
        -> filters (to filter an important entry for the futher update)
        -> files
        -> put_req and patch_req (to know whether you want to update the whole entry or an equal part)
        """

        if self.url != None and self.put != None:
            raise SettingsError


        if self.url != None or self.put != None:

            pars = self._get_params(params, filters)

            if self.content_type == "json":
                if patch_req:
                    new_data = self._PATCH_request(params=pars, files=files,json_data=json_data)
                elif put_req:
                    new_data = self._PUT_request(params=pars, files=files,json_data=json_data)   
                else:
                    raise HttpMethodError
            else:
                raise ContentTypeError
            
            if new_data.status_code != 200:
                raise InvalidDataError
            return None

        raise UpdateDataError


    def create_data(self, params:dict = None, filters:dict = None, data:dict = None, files: dict = None) -> bool:
        """Creates new entry.Can take such params as:
        -> json-data
        -> files
        """

        if self.url != None and self.post != None:
            raise SettingsError

        if data:
            pars = self._get_params(params, filters)
            data_post = self._POST_request(params=pars, files=files, json_data=data)
        return False


    def __repr__(self):
        return "%s" % (self.__class__)


    def __str__(self):
        if self.__class__.__doc__ != None:
            return "Class - %s\nDocString - %s" % (self.__class__.__name__, self.__class__.__doc__)
        return "Class - %s" % (self.__class__.__name__)
