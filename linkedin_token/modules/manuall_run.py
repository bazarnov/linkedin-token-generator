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
code = "AQQXTV5lCZlRHJi16nmTCwv752zxco2LY2GvGi4LWyAWh3jHwLTWqcvq16A2F2eebC7ERnHnZeRnhmeZ1unkPBUc7Cnn0McsLjpz-61QoSB8xyobmGhI1fDxYOIk6V1wYu1v6FLGS_ZA86prLEdC_VTX7Uf16K-s5xQXFNo9tRLWYF-RRbthh2cMk1D0cmD64fmjMiDLFbXXI7FAwfc"
token = instance.get_access_token(config, code)
print(token)