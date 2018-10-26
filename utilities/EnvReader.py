from utilities.Errors import EnvError
import os

try:
    with open('.env') as f:
        env_arr = f.readlines()

    for couple in env_arr:
        os.environ[couple.split("=")[0].strip()] = couple.split("=")[1].strip()

except Exception:
    raise EnvError()


def get_api_key():
    """
    :return: Google API KEY
    """
    try:
        return os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    except Exception:
        raise EnvError()
