import json
from jose import jwt
from urllib.request import urlopen

# Configuration
# UPDATE THIS TO REFLECT YOUR AUTH0 ACCOUNT
# AUTH0_DOMAIN = 'fsnd.auth0.com'
# ALGORITHMS = ['RS256']
# API_AUDIENCE = 'image'

AUTH0_DOMAIN = 'fsnd-auth0-test.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'webapp-api'

'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# PASTE YOUR OWN TOKEN HERE
# MAKE SURE THIS IS A VALID AUTH0 TOKEN FROM THE LOGIN FLOW
# token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik56Z3lSVFZEUmpKQ1FrUkJSRGN3TjBReFJUQTFPVUl5UlRORk9EQXhPVGMwTmpjNU9USkVPQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVkMDNkM2U2NzI2YjhmMGNiNGJmNzFjOSIsImF1ZCI6ImltYWdlIiwiaWF0IjoxNTYwNTU2MTc0LCJleHAiOjE1NjA1NjMzNzQsImF6cCI6ImtpNEI2alprdUpkODdicEIyTXc4emRrajFsM29mcHpqIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6aW1hZ2VzIiwicG9zdDppbWFnZXMiXX0.ENxNT1lo_sX9rpgmGJmiu14lugmYXqb8siJwC1nPuGSb_ycK02KyS5IkA-YkhySMBcDD5IJfawPkJNmJPtUAB1wYVP8hlNsBuvLjtYxzH_VHNeXzVXWQvM7RiuPwrmWJmJN2onmZPh3bjiUZxvyAp0Yp0Rvm54SsiDjO_Dj1Qx-Az_Zjo-mY2ECfFgAo0ifnqDMIgE5YDZ3uOzMni4oEU5Ok-TrQOSwyfJyUC1KQ7ubQ-Bnbh-0Aii9UK9R4JBH7iIMva8_edQkgR4MuRXatYhsqvHsxQ2Iv5rjMmTAmjknsYWE5VYrzafRGVigbPD9A6ELEnyjADBQ9vMtSdPQe2w"

token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlpvOWpPcXZXT3ZBYnN3bzZFWVQxayJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYXV0aDAtdGVzdC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBmOWQwNzM4ZTMxZDUwMDY5ZjRmOThlIiwiYXVkIjoid2ViYXBwLWFwaSIsImlhdCI6MTYyNzA2MTA2OSwiZXhwIjoxNjI3MDY4MjY5LCJhenAiOiIzUDM4bGdBZXJZeWFjOEZTVUU2aTdnS0l5ZVg2VU00VSIsInNjb3BlIjoiIn0.c8S6oHC5QfCyGHXqC33WjPikoRtR6y9L86vo0lD8pG6VjAjlDoCMRtUdbJMyKl79sY1eP8vLT03_gFTC5XkLLAy1pK_7dpXyhMoHyaen2ciWaJpfLuZZcm0WTHY4HkmIWSv5EXbIqr79---FC-Niu8wFp_h7w9C6CG2ubiLKW0OQTff7-SO5iSWAC8gfoUXsCsCzT3X8ktQG-AlMW11bEr8l7g9evQO3pmu1ySzkmxOShTOPaaIfH-YtZVJUSPPA261hyInrhgkZKrtdlLwyjKcvyUPb0XcOzslyHiJH5_ohj5yTysc-lTrScU4RTOZg3hF7Ftmwj0C_bVbtwI20eQ"


## Auth Header
def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # print(f'\njsonurl: {jsonurl}')
    # print(f'\njwks: {jwks}')


    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    # print(f'\nunverified_header: {unverified_header}')

    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # print(f'\nrsa_key: {rsa_key}')

    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            
            print(f'\nALGORITHMS: {ALGORITHMS}')
            print(f'\nAPI_AUDIENCE: {API_AUDIENCE}')
            print(f'\nAUTH0_DOMAIN : {AUTH0_DOMAIN}')
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

payload = verify_decode_jwt(token)
print(f'\npayload : {payload}')