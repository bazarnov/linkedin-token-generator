from linkedin_token.modules.entrypoint import read_config
from linkedin_token.modules import LinkedInAuth 

# DEFINE THE PATH TO CONFIG
PATH_TO_CONFIG = "/Users/bazarnov/Desktop/linkedin_token/secrets/config.json"

# PREPARE ENV
instance = LinkedInAuth()
config = read_config(PATH_TO_CONFIG)

# ATTEMPT 1 - use the Login > Get Auth Code > Get Access Token
# IF THIS ATTEMPT IS FAILED WITH `FailAuthCode: ('Failed. Follow the link to verify your authentication...)'
# THEN FOLLOW ATTEMPT 2 by using the link and authenticate using browser, obtain the Auth-Code manually and use it,
# IN ATTEMPT 2
token = instance.get_access_token(config)
print(token)

# ATTEMPT 2 - use  the AUTH_CODE provided inside the redirect_uri link to get the access_token
code = "YOUR_AUTH_CODE_HERE"
token = instance.get_access_token(config, code)
print(token)