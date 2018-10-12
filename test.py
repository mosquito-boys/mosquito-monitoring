from environs import Env
import os
env = Env()
env.read_env()

SECRET_KEY = os.getenv("TEST")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")