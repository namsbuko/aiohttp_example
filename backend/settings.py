from os.path import isfile
from envparse import env


if isfile('.env'):
    env.read_envfile('.env')


JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')
API_URL = env.str('API_URL')

REDIS_HOST = env.str('REDIS_HOST')
REDIS_PORT = env.int('REDIS_PORT')
