import re
class Config:
    SECRET_KEY = '066132ac261b515e278aae0ac6edabb7'
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    PASSWORD_REGEX_UPPERCASE = re.compile(r'[A-Z]')
    PASSWORD_REGEX_NUMBER = re.compile(r'[0-9]')
