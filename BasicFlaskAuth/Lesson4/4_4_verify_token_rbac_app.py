from flask import Flask, request, abort
from functools import wraps
import json
from jose import jwt
from urllib.request import urlopen


app = Flask(__name__)

# Pre-requisite:  You need to register an Auth0 account (free), and do the following:
# 1. Select a unique tenant domain
# 2. Create a new, single page web application
# 3. Create a new API

# this is your Auth0 domain name
AUTH0_DOMAIN = 'fsnd-auth0-test.us.auth0.com'
# leave this alone, no change
ALGORITHMS = ['RS256']
# Your Auth0 API name
API_AUDIENCE = 'webapp-api'

'''
IMPORTANT: You need to get your token by typing in the following: 
    https://{{AUTH0_DOMAIN}}/authorize?audience={{API_AUDIENCE}}&response_type=token&client_id={{CLIENT_ID}}&redirect_uri={{CALLBACK_URI}}

    Replace the curly braces with their respective values:
    - AUTH0_DOMAIN, CLIENT_ID, and CALLBACK_URL can be found under `Basic Information` under your AUTH0 application dashboarD
    - API-AUDIENCE can be found under your AUTH0 Application > APIs page - get the  'API Audience' value of your API.

   To test this python program, you need the following:
   - start up this Flask application  
   - open your browser, typing in the following AUTH0 URL call and SUBMIT it: 
    https://{{AUTH0_DOMAIN}}/authorize?audience={{API_AUDIENCE}}&response_type=token&client_id={{CLIENT_ID}}&redirect_uri={{CALLBACK_URI}}

   - the token returned from the URL posted in the IMPORTANT' section above
   - Download Postman app, open the app and do the following:
       - do 'Create new HTTP Request' - a new window will open
       - in the 'Enter Request URL' box, enter `http://127.0.0.1:5001/headers`
       - click on Authorization right below the URL, change type from 'No Auth' to 'Bearer Token'
       - once 'Bearer Token' is selected, on the right pane look for Token and enter the token value:
          - ERROR test - enter ANY value in the token field then hit SEND button next to the request URL in Postman, it will return 401
          - SUCCESS test: good scenario, enter the token value provided in the browser URL, then hit SEND button next to the request URL in Postman

              - TIP:  If you get an error that says your token is not accepted, you need to resubmit the AUTH0 URL and pick up the new token returned,
                      replace the bearer token in Postman with the new value, and hit SEND again        
'''

'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# Auth0  Auth Header
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
            
            # print(f'\nALGORITHMS: {ALGORITHMS}')
            # print(f'\nAPI_AUDIENCE: {API_AUDIENCE}')
            # print(f'\nAUTH0_DOMAIN : {AUTH0_DOMAIN}')
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


# this function gets the bearer token value you entered in Postman
def get_header_token():
    # @TODO unpack the header request
    if "Authorization" not in request.headers:
        abort(401)

    auth_header = request.headers["Authorization"]
    header_parts = auth_header.split(' ')
  
    if len(header_parts) != 2:
        abort(401)
    else:
        if header_parts[0].lower() != 'bearer':
            abort(401)
    return header_parts[1]

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)
    else:
        if permission not in payload['permissions']:
            abort(403)  # Forbidden
    # return True

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrappers(*args, **kwargs):
            jwt = get_header_token()
            try:
                payload = verify_decode_jwt(jwt)
            except:
                abort(401)

            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)
        return wrappers
    return requires_auth_decorator

@app.route('/headers')
@requires_auth('write:database')
def headers(payload):
    print(f'\npayload : {payload}')
    return 'not implemented'
