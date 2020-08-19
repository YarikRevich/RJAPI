import requests
from .utils import Utils
from .exception import (UpdateDataError,
                        URLStatusCodeError,
                        SettingsError,
                        ContentTypeError,
                        InvalidDataError,
                        HttpMethodError)


class BaseAPIData(Utils):
    """Base RJAPI class where there is written main methods to get and update data"""


    def get_data(self,params: dict = None,filters: dict = None) -> "json":
        """Returns serialized json data"""
        pars = self._get_params(params,filters)
        if self.url != None:
            data = requests.get(self.url + pars,auth=("yarik","yariksun4002"))
        else:
            data = requests.get(self.get + pars,auth=("yarik","yariksun4002"))
        if data.status_code != 200:
            raise URLStatusCodeError
        return data.json()


    def update_data(self, json_data: dict,params: dict = None, filters:dict = None,put_req: bool = False, patch_req: bool = False) -> None:
        """Updates data"""

        
        if self.url != None or self.put != None:
            if self.url != None and self.put != None:
                raise SettingsError
            
            pars = self._get_params(params,filters)
            if put_req or patch_req:
                if self.url != None:
                    if self.content_type == "json":
                        if self.auth_data:
                            if patch_req:
                                new_data = requests.patch(self.url + pars, auth=self.auth_data, json=json_data)
                            else:
                                new_data = requests.put(self.url + pars, auth=self.auth_data, json=json_data)
                        else:
                            if patch_req:
                                new_data = requests.patch(self.url + pars, json=json_data)
                            else:
                                new_data = requests.put(self.url + pars, json=json_data)
                    else:
                        raise ContentTypeError 
                else:
                    if self.content_type == "json":
                        if self.auth_data:
                            if patch_req:
                                new_data = requests.patch(self.patch + pars, auth=self.auth_data, json=json_data)
                            else:
                                new_data = requests.put(self.put + pars, auth=self.auth_data, json=json_data)
                        else:
                            if patch_req:
                                new_data = requests.patch(self.patch + pars, json=json_data)
                            else:
                                new_data = requests.put(self.put + pars, json=json_data)
                    else:
                        raise ContentTypeError
            else:
                raise HttpMethodError
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