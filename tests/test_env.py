from utilities.EnvReader import EnvReader
from utilities.Errors import EnvError

EnvReader = EnvReader()

if not isinstance(EnvReader.get_api_key(), str):
    raise EnvError()
else:
    print("Success!")
