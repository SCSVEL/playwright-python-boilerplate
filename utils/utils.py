import dotenv
from os import environ

def get_env(var_name: str):
    dotenv.load_dotenv(".\envconfig\TST.env")

    return environ.get(var_name, "")
