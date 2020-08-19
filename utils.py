

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