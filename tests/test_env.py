from utilities.EnvReader import get_api_key
from utilities.Errors import EnvError

if not isinstance(get_api_key(), str):
    raise EnvError()
else:
    print("Success!")
