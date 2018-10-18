class InsectNotFound(Exception):

    def __init__(self):
        Exception.__init__(self, "No insect was found in the picture")
