from jose import jwt

SECRET_KEY = "secret"
def encode_jwt(user_id):
    #encode based on user_id
    payload = {
        "sub": user_id
    }
    encoded_jwt_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return encoded_jwt_token

print(encode_jwt("sarah_m"))