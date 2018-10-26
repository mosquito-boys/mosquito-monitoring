class InsectNotFound(Exception):
    """
    Error raised if Google API didn't recognized any insect in the picture
    """
    def __init__(self):
        Exception.__init__(self, "No insect was found in the picture")


class EnvError(Exception):
    """
    Error for .env loading into project
    """
    def __init__(self):
        Exception.__init__(self, "Error during environment loading. Please check your .env file")

class APIQuotaExceeded(Exception):
    """
    The google API has exceeded quota
    """
    def __init__(self):
        Exception.__init__(self, "Google API has exceeded max quota. Please wait a minute before requesting again")
