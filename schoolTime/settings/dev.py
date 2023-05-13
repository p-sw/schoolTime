from .base import *
from secrets import token_hex

DEBUG = True

SECRET_KEY = token_hex(50)

ALLOWED_HOSTS = ['*']
