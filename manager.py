import os

from dotenv import load_dotenv
from outline_vpn.outline_vpn import OutlineVPN

load_dotenv()

API_URL = os.getenv("API_URL")
CERTSHA256 = os.getenv("CERTSHA256")


client = OutlineVPN(API_URL, CERTSHA256)  # type: ignore
client.get_server_information()


def byte_to_gb(byte: int = 0):
    if byte == (0 or None):
        return 0
    else:
        return (byte / 1024**3).__round__(2)


def get_keys():
    keys = {}
    for key in client.get_keys():
        keys[key.name] = [key.access_url, byte_to_gb(key.used_bytes)]
    return keys


def get_key_id(name):
    for key in client.get_keys():
        if key.name == name:
            return key.key_id


def add_key(name):
    keys = get_keys()
    if name in keys:
        return
    new_key = client.create_key(name=name)
    return [new_key.name, new_key.access_url]


def delete_key(name):
    return client.delete_key(get_key_id(name))

