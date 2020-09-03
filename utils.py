import requests
from requests.exceptions import ConnectionError
import time


class Utils:
    """Takes all the utils for the functionality
    -> Generator of the params by gotten data

    """

    @staticmethod
    def _get_params(params: dict, filters: dict) -> str:
        """
        Checks whether there are any params
        If they do,returns them

        """

        def get_param_string() -> str:
            """Returns the str which contains all the entered parrams"""

            pars = ""
            if params:
                for one in params:
                    pars += f"{params.get(one,'')}/"
                return pars
            return pars
            

        def get_filter_string(param_string: str = "") -> str:
            """Returns the str which contains all the parrams and filters"""
            
            param_string += "?"
            for index,item in enumerate(filters.items()):
                param_string += "%s=%s&" % (item[0],item[1])
                if index == len(filters) - 1:
                    param_string += "%s=%s" % (item[0],item[1])
            return param_string


        param_string = get_param_string()
        if filters:
            return get_filter_string(param_string)
        return param_string


    def _GET_request(self, params: dict = None) -> object:
        """Does GET request to the url or get attributes which contain
        urls to communicate with API
        """

        def _sub_GET_request(url: str) -> object:
            """A sub func which does a get request"""

            try:
                return requests.get(
                    url + (params if params is not None else ""),
                    auth=(self.auth_data if hasattr(self, "auth_data") else None),
                    headers={"User-Agent":self.user_agent})
            except ConnectionError:
                time.sleep(.1)
                return _sub_GET_request(url)


        if self.url is not None:
            return _sub_GET_request(self.url)
        return _sub_GET_request(self.get)

    
    def _PUT_request(self, params: dict = None, files: dict = None, json_data: dict = None) -> object:
        """Does PUT request to the url or put attributes which contain
        urls to communicate with API
        """

        def _sub_PUT_request(url: str) -> object:
            """A sub func which does a put request"""

            try:
                return requests.put(
                    url + (params if params else ""),
                    auth = (self.auth_data if hasattr(self, "auth_data") else None),
                    files = (files if files else None),
                    json = (json_data if json_data else None),
                    headers={"User-Agent":self.user_agent})
            except ConnectionError:
                time.sleep(.1)
                return _sub_PUT_request(url)


        if self.url is not None:
            return _sub_PUT_request(self.url)
        return _sub_PUT_request(self.put)

    
    def _PATCH_request(self, params: dict = None, files:dict = None, json_data: dict = None) -> object:
        """Does PATCH request to the url or patch attributes which contain
        urls to communicate with API
        """

        def _sub_PATCH_request(url: str) -> object:
            """A sub func which does a patch request"""

            try:
                return requests.patch(
                    url + (params if params else ""),
                    auth = (self.auth_data if hasattr(self, "auth_data") else None),
                    files = (files if files else None),
                    json = (json_data if json_data else None),
                    headers={"User-Agent":self.user_agent})
            except ConnectionError:
                time.sleep(.1)
                return _sub_PATCH_request(url)


        if self.url is not None:
            return _sub_PATCH_request(self.url)
        return _sub_PATCH_request(self.patch)


    def _POST_request(self, params: dict = None, files: dict = None, json_data: dict = None) -> object:
        """Does POST request to the url or post attributes which contain
        urls to communicate with API
        """

        def _sub_POST_request(url: str) -> object:
            """A sub func which does a post request"""

            try:
                return requests.post(
                    url + (params if params else ""),
                    auth = (self.auth_data if hasattr(self, "auth_data") else None),
                    files = (files if files else None),
                    data = (json_data if json_data else None),
                    headers={"User-Agent":self.user_agent})
            except ConnectionError:
                time.sleep(.1)
                return _sub_POST_request(url)


        if self.url is not None:
            return _sub_POST_request(self.url)
        return _sub_POST_request(self.post)


    def _DELETE_request(self, params: dict = None) -> None:
        """A helpful method to make a delete request"""

        def _sub_DELETE_request(url: str) -> object:
            """A sub func which does a delete request"""

            try:
                return requests.delete(
                    url + (params if params else ""),
                    auth = (self.auth_data if hasattr(self, "auth_data") else None),
                    headers={"User-Agent":self.user_agent})
            except ConnectionError:
                time.sleep(.1)
                return _sub_DELETE_request(url)

        if self.url is not None:
            return _sub_DELETE_request(self.url)
        return _sub_DELETE_request(self.delete)