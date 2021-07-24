# NOTE: this program does not use Flask

import bcrypt

# refer to bcrypt package documentation on https://github.com/pyca/bcrypt/

# note that passwords need to be in converted to binary format before getting hashed
password = b"studyhard"

# Hash a password for the first time, with a certain number of rounds - bycrpt.gensalt() allows you to specify the number
# The higher the round number the better; but in practice, the optimal number depends on machine's processor (google for further info)
salt = bcrypt.gensalt(14)
hashed = bcrypt.hashpw(password, salt)
# print them to see how the values look like
print(f'salt: {salt} \thashed: {hashed}')   


# use bcrypt.checkpw(password,hashed_value) to verify the password
# here is a little exercise to see which one from a set of passwords matches a given hash
hash_value = b'$2b$14$EFOxm3q8UWH8ZzK1h.WTZeRcPyr8/X0vRfuL3/e9z7AKIMnocurBG'
# again, note that passwords need to be cast from strings to bytes for bcrypt to work
passwords = [b'securepassword', b'udacity', b'learningisfun']
# run to see which password in the list matches the hash_value
for password in passwords:
    if bcrypt.checkpw(password, hash_value):
        print(f'The password {password} matches the hashed value {hash_value}')
        break
