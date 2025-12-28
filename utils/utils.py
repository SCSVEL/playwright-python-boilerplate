import dotenv
from os import environ


class Utils:    
    @staticmethod
    def get_env(var_name: str) -> str:
        # Load default test env file if one isn't already loaded.
        dotenv.load_dotenv(".\envconfig\TST.env")
        return environ.get(var_name, "")


def get_env(var_name: str) -> str:    
    return Utils.get_env(var_name)
