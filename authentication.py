import base64
import json
import random
from datetime import datetime, timedelta
import re
from cryptography.fernet import Fernet
import quart
from quart import request


def encrypt_password(shift, message):
    encrypted_message = ""
    for char in message:
        if char.isalpha():  # Check if the character is an alphabet
            shifted_char = chr(((ord(char) - 65 + shift) % 26) + 65) if char.isupper() else chr(
                ((ord(char) - 97 + shift) % 26) + 97)
            encrypted_message += shifted_char * 2
        elif char.isdigit():  # Check if the character is a digit
            shifted_digit = str((int(char) + shift) % 10)
            encrypted_message += shifted_digit * 2
        else:
            encrypted_message += char
    return encrypted_message


def decrypt_password(shift, encrypted_message):
    decrypted_message = ""
    for i in range(0, len(encrypted_message), 2):
        char = encrypted_message[i]
        if char.isalpha():
            shifted_char = chr(((ord(char) - 65 - shift) % 26) + 65) if char.isupper() else chr(
                ((ord(char) - 97 - shift) % 26) + 97)
            decrypted_message += shifted_char
        elif char.isdigit():
            shifted_digit = str((int(char) - shift) % 10)
            decrypted_message += shifted_digit
        else:
            decrypted_message += char
    return decrypted_message


def token_validator():
    ...


def token_generator(user):
    time_to_play = datetime.now() + timedelta(minutes=5)
    btoken = str(format(time_to_play.strftime("%Y%m%d%H%M%S")))
    btoken += user
    shift = 3
    e_btoken = encrypt_password(shift, btoken)
    print(e_btoken)
    return {"Bearer": e_btoken}


async def credential_checker():
    credentials = await request.json
    # print(credentials)

    with open("auth_users.json", "r") as file:
        data: list = json.load(file)

    credentials: dict
    username: str = credentials.get("user")
    password: str = credentials.get("password")

    for user in data:
        if user.get("user") == username:
            shift = 3
            decrypted_pw = decrypt_password(shift, user.get("password"))

            if decrypted_pw == password:
                print("Found")
                return credentials

    raise Exception("Incorrect credentials")


async def auth_interceptor():
    headers = request.headers
    bearer = headers.get('Authorization')
    e_btoken = bearer.split()[1][0:28]
    shift = 3
    print(bearer)
    btoken = decrypt_password(shift, e_btoken)
    print(btoken)
    if int(btoken) < int(datetime.now().strftime("%Y%m%d%H%M%S")):
        print("old token")
        raise Exception("Old token")


def create_account(credentials):
    with open("auth_users.json", "r") as file:
        data: list = json.load(file)

    credentials: dict
    username: str = credentials.get("user")
    password: str = credentials.get("password")

    shift = 3
    hashed_pw = encrypt_password(shift, password)
    credentials["password"] = hashed_pw

    for user in data:
        if user.get("user") == username:
            raise Exception("Username already chosen")

    if len(username) < 3 or len(username) > 22:
        raise Exception("Name too long or too short")
    if len(password) < 8 or len(password) > 30:
        raise Exception("Password too long or too short")
    if re.search(r"[A-Z]", password) is None or re.search(r"\d", password) is None or re.search(r"[a-z]", password) is None:
        raise Exception("Password too weak")

    btoken = token_generator(credentials.get("user"))

    with open("auth_users.json", "w") as file:
        credentials["token"] = btoken
        data.append(credentials)
        json.dump(data, file, indent=4)

    return btoken
