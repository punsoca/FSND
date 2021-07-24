from flask import Flask, request, abort
from functools import wraps

app = Flask(__name__)

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

def requires_auth(f):
    @wraps(f)
    def wrappers(*args, **kwargs):
        jwt = get_header_token()
        return f(jwt, *args, **kwargs)
    return wrappers

@app.route('/headers')
@requires_auth
def headers(jwt):
    print(jwt)
    return 'not implemented'
