from Crypto.Cipher import AES
from secrets import token_bytes
import rsa
import DataProcessing as dp


def gen_rsa_keys():
    return rsa.newkeys(500)


def gen_session_key():
    return token_bytes(16)
