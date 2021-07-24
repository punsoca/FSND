# program that illustrates JSON web token validation
import jwt     # need to pip3 install pyJWT to make this lib available 
import base64
# Init our Data
payload = {'park':'madison square'}
algo = 'HS256' #HMAC-SHA 256
secret = 'learning'

# Encode a JWT
encoded_jwt = jwt.encode(payload, secret, algorithm=algo)
print(f'\nencoded_jwt = {encoded_jwt}')

# Decode a JWT
decoded_jwt = jwt.decode(encoded_jwt, secret, algorithms=algo, verify=True)
print(f'decoded_jwt = {decoded_jwt}')

#--
#-- now test these two tokens, check which of these tokens may have been tampered with
#--

# encoded_jwt2
encoded_jwt2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXJrIjoiY2VudHJhbCBwYXJrIn0.H7sytXDEHK1fOyOYkII5aFfzEZqGIro0Erw_84jZuGc'
print(f'\nencoded_jwt2 = {encoded_jwt2}')
decoded_jwt2 = jwt.decode(encoded_jwt2, secret, algorithms=algo, verify=True)
print(f'decoded_jwt2 = {decoded_jwt2}')

# encoded_jwt3
encoded_jwt3 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXJrIjoiYmF0dGVyeSBwYXJrIn0.bQEjsBRGfhKKEFtGhh83sTsMSXgSstFA_P8g2qV5Sns'
print(f'\nencoded_jwt3 = {encoded_jwt3}')
decoded_jwt3 = jwt.decode(encoded_jwt3, secret, algorithms=algo, verify=True)
print(f'decoded_jwt2 = {decoded_jwt2}')
