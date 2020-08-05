
class URLStatusCodeError(Exception):
    
    def __str__(self):
        return "You have written invalid url"

class InvalidDataError(Exception):

    def __str__(self):
        return "You have passed invalid data,check it again"

class UpdateDataError(Exception):

    def __str__(self):
        return "You haven't passed neither 'url' nor 'put'"

class SettingsError(Exception):

    def __str__(self):
        return "It seems that you have written both 'url' and 'put' "

class ContentTypeError(Exception):

    def __str__(self):
        return "You have written wrong content_type"

class IdError(Exception):

    def __str__(self):
        return "It seems that there is no an id key in your json.Check it up!"