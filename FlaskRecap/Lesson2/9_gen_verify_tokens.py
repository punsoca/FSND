# Watch Videos from Udacity Lesson 2: Identity and Authentication (Flask Auth0)
# This program that illustrates JSON web token validation

# need to run 'pip3 install pyJWT' - preferably in your virtual env - to make the `jwt` lib available 
import jwt

import base64, os

#--  1. how to generate, encode, and decode a token

# Init our Data for test 1
payload = {'park':'madison square'}
algo = 'HS256' #HMAC-SHA 256
secret = 'learning'

# clear screen
os.system('clear')

print('Test1:  Encoding our data with algorithm, payload, and secret:')
print(f'\nData: payload: {payload}\talgo: {algo}\tsecret: {secret}')


# Encode a JWT 
encoded_jwt = jwt.encode(payload, secret, algorithm=algo)
print(f'\nencoded_jwt = {encoded_jwt}')
# Decode a JWT - this should return the payload value "{'park':'madison square'}"
decoded_jwt = jwt.decode(encoded_jwt, secret, algorithms=algo, verify=True)
print(f'decoded_jwt (returns the payload value) = {decoded_jwt}')



#-- 2. verify token if signature is valid 
#-- now test these two tokens, check which of these tokens may have been tampered with
#-- These were signed with the secret 'learning'
#--

test_encoded_jwts = [ 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXJrIjoiY2VudHJhbCBwYXJrIn0.H7sytXDEHK1fOyOYkII5aFfzEZqGIro0Erw_84jZuGc',
                      'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXJrIjoiYmF0dGVyeSBwYXJrIn0.bQEjsBRGfhKKEFtGhh83sTsMSXgSstFA_P8g2qV5Sns'  
                    ]
print('\nTest2:  Check which of the following JWTs may have been tampered with:\n')

for idx, encoded in enumerate(test_encoded_jwts, start=1):
    try:
        print(f'test_encoded_jwt{idx}: {encoded}')
        decoded_value = jwt.decode(encoded, secret, algorithms=algo, verify=True)
    except jwt.exceptions.InvalidSignatureError:
        print(f"test_encoded_jwt{idx} =  Signature verification failed for test_encoded_jwt1\n")
    else:
        print(f'test_encoded_jwt{idx} = {decoded_value}\n')
