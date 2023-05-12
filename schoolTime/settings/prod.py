from .base import *
from secrets import token_hex

DEBUG = False

SECRET_KEY = token_hex(50)

ALLOWED_HOSTS = ["schultime.sserve.work"]
