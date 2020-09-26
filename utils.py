import requests
import aiohttp
import asyncio
from aiohttp.client_exceptions import ClientConnectionError
from aiohttp import FormData
from requests.exceptions import ConnectionError


class Utils:
    """Takes all the utils for the functionality."""

    @staticmethod
    async def _get_params(params: dict, filters: dict) -> str:
        """Checks whether there are any params If they do,returns them."""

        async def get_param_string() -> str:
            """Returns the str which contains all the entered parrams."""

            pars = ""
            if params:
                for one in params:
                    pars += f"{params.get(one,'')}/"
                return pars
            return pars
            

        async def get_filter_string(param_string: str = "") -> str:
            """Returns the str which contains all the parrams and filters."""
            
            param_string += "?"
            for index,item in enumerate(filters.items()):
                param_string += "%s=%s&" % (item[0],item[1])
                if index == len(filters) - 1:
                    param_string += "%s=%s" % (item[0],item[1])
            return param_string


        param_string = await get_param_string()
        if filters:
            return await get_filter_string(param_string)
        return param_string


    async def _GET_request(self, params: dict = None) -> object:
        """Does GET requests."""

        async def _sub_GET_request(url: str) -> object:
            """A sub func which does a get request."""

            async with aiohttp.ClientSession(
                auth=aiohttp.BasicAuth(
                    self.auth_data[0], self.auth_data[1] if hasattr(self, "auth_data") else None
                    ),
                headers={"User-Agent":self.user_agent}
                ) as session:
                async with session.get(url + (params if params is not None else "")) as response:
                    
                    return (await response.json(), response.status)
                    

        if self.url is not None:
            return await _sub_GET_request(self.url)
        return await _sub_GET_request(self.get)

    
    async def _PUT_request(self, params: dict = None, 
                            files: dict = None, json_data: dict = None) -> object:
        """Does PUT requests."""

        async def _sub_PUT_request(url: str) -> object:
            """A sub func which does a put request."""

            return await self.mechanism_of_sending_data(url, params, "put", json_data, files)


        if self.url is not None:
            return await _sub_PUT_request(self.url)
        return await _sub_PUT_request(self.put)

    
    async def _PATCH_request(self, params: dict = None, 
                            files:dict = None, json_data: dict = None) -> object:
        """Does PATCH requests"""

        async def _sub_PATCH_request(url: str) -> object:
            """A sub func which does a patch request"""

            return await self.mechanism_of_sending_data(url, params, "patch", json_data, files)
       

        if self.url is not None:
            return await _sub_PATCH_request(self.url)
        return await _sub_PATCH_request(self.patch)


    async def _POST_request(self, params: dict = None, 
                            files: dict = None, json_data: dict = None) -> object:
        """Does post requests"""

        async def _sub_POST_request(url: str) -> object:
            """A sub func which does a post request"""

            return await self.mechanism_of_sending_data(url, params, "post", json_data, files)


        if self.url is not None:
            return await _sub_POST_request(self.url)
        return await _sub_POST_request(self.post)


    async def _DELETE_request(self, params: dict = None) -> None:
        """A helpful method to make a delete request"""

        async def _sub_DELETE_request(url: str) -> object:
            """A sub func which does a delete request"""

            async with aiohttp.ClientSession(
                auth=aiohttp.BasicAuth(
                    self.auth_data[0], self.auth_data[1] if hasattr(self, "auth_data") else None
                    ),
                headers={"User-Agent":self.user_agent}
                ) as session:
                async with session.delete(
                    url + (params if params else "")
                ) as response:
                    return response.status


        if self.url is not None:
            return await _sub_DELETE_request(self.url)
        return await _sub_DELETE_request(self.delete)


    async def mechanism_of_sending_data(self, url: str, 
                                        params: str, http_method: str, 
                                        json_data: dict, files: dict):
        """It is the main component of all the requests.
        It does forming of all the data or just one of its
        part. Also, it can be used for methods: POST, PATCH, PUT

        """
    
        async def form_all_data():
            """Forms both image and json data for the uploading"""

            data = FormData()
            for key, item in json_data.items():
                data.add_field(name=key, value=item, content_type="application/json")
            for key, item in files.items():
                data.add_field(name=key, value=item[1], filename=item[0], content_type="multipart/form-data")
            return data

        async def form_image():
            """Forms image for the uploading"""

            data = FormData()
            for file_name in files:
                data.add_field("visit_image", value=files[file_name][1], filename=files[file_name][0], content_type="multipart/form-data")
            return data


        async with aiohttp.ClientSession(
            auth=aiohttp.BasicAuth(
                self.auth_data[0], self.auth_data[1] if hasattr(self, "auth_data") else None
                ),
            headers={"User-Agent":self.user_agent}) as session:
            async with getattr(session, http_method)(
                url + (params if params else ""),
                data = await form_all_data() if (files and json_data) else json_data if json_data else await form_image() if files else None) as response:
                return (await response.json(), response.status)
