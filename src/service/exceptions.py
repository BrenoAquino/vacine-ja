class UnavailableTokenException(Exception):
    """ Exception for when cannot get a token from the server """
    pass

class InvalidSearchReponseException(Exception):
    """ Exception for when the search response is invalid """
    pass