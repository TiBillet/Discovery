import hashlib
import json, base64
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def data_to_b64(data: dict or list) -> bytes:
    data_to_json = json.dumps(data)
    json_to_bytes = data_to_json.encode('utf-8')
    bytes_to_b64 = base64.urlsafe_b64encode(json_to_bytes)
    return bytes_to_b64

def b64_to_data(b64: bytes) -> dict or list:
    b64_to_bytes = base64.urlsafe_b64decode(b64)
    bytes_to_json = b64_to_bytes.decode('utf-8')
    json_to_data = json.loads(bytes_to_json)
    return json_to_data



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    x_real_ip = request.META.get('HTTP_X_REAL_IP')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    elif x_real_ip:
        ip = x_real_ip
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def get_public_key(public_key_pem: str) -> rsa.RSAPublicKey | bool:
    try:
        # Charger la clé publique au format PEM
        public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'), backend=default_backend())

        # Vérifier que la clé publique est au format RSA
        if not isinstance(public_key, rsa.RSAPublicKey):
            return False
        return public_key

    except Exception as e:
        logger.error(f"Erreur de validation get_public_key : {e}")
        raise e


def hash_hexdigest(utf8_string):
    return hashlib.sha256(utf8_string.encode('utf-8')).hexdigest()

def fernet_encrypt(message: str) -> str:
    message = message.encode('utf-8')
    encryptor = Fernet(settings.FERNET_KEY)
    return encryptor.encrypt(message).decode('utf-8')


def fernet_decrypt(message: str) -> str:
    message = message.encode('utf-8')
    decryptor = Fernet(settings.FERNET_KEY)
    return decryptor.decrypt(message).decode('utf-8')


def rsa_encrypt_string(utf8_string=None, public_key: rsa.RSAPublicKey=None) -> str:
    message = utf8_string.encode('utf-8')
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.urlsafe_b64encode(ciphertext).decode('utf-8')

def rsa_decrypt_string(utf8_enc_string: str, private_key: rsa.RSAPrivateKey) -> str:
    ciphertext = base64.urlsafe_b64decode(utf8_enc_string)
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode('utf-8')

def sign_message(message: bytes = None,
                 private_key: rsa.RSAPrivateKey = None) -> bytes:
    # Signer le message
    signature = private_key.sign(
        message,
        padding=padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        algorithm=hashes.SHA256()
    )
    return base64.urlsafe_b64encode(signature)


def verify_signature(public_key: rsa.RSAPublicKey,
                     message: bytes,
                     signature: str) -> bool:
    # Vérifier la signature
    try:
        public_key.verify(
            base64.urlsafe_b64decode(signature),
            message,
            padding=padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            algorithm=hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

