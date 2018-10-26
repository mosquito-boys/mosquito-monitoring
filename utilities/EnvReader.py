from utilities.Errors import EnvError


class EnvReader:
    """
    Access the environment variables
    """
    def __init__(self):
        try:
            with open('.env') as f:
                env_arr = f.readlines()

            env_dict = {}

            for couple in env_arr:
                env_dict[couple.split("=")[0].strip()] = couple.split("=")[1].strip()

            self.__env_dict = env_dict

        except Exception:
            raise EnvError()

    def get_api_key(self):
        """
        :return: Google API KEY
        """
        try:
            return self.__env_dict["GOOGLE_APPLICATION_CREDENTIALS"]
        except Exception:
            raise EnvError()
