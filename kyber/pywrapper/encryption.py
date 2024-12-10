import ctypes
import numpy as np
import os

# Load Kyber shared library
current_dir = os.path.dirname(os.path.abspath(__file__))
libkyber_path = os.path.join(current_dir, "../ref/libkyber.so")
kyber_lib = ctypes.CDLL(libkyber_path)

# Define Kyber constants
KYBER_PUBLICKEYBYTES = 800
KYBER_SECRETKEYBYTES = 1632
KYBER_CIPHERTEXTBYTES = 768
KYBER_SSBYTES = 32

# Define Kyber function prototypes
kyber_lib.crypto_kem_keypair.restype = ctypes.c_int
kyber_lib.crypto_kem_keypair.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8)]

kyber_lib.crypto_kem_enc.restype = ctypes.c_int
kyber_lib.crypto_kem_enc.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8)]

kyber_lib.crypto_kem_dec.restype = ctypes.c_int
kyber_lib.crypto_kem_dec.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8)]

# Kyber Functions
def generate_keypair():
    pk = np.zeros(KYBER_PUBLICKEYBYTES, dtype=np.uint8)
    sk = np.zeros(KYBER_SECRETKEYBYTES, dtype=np.uint8)
    result = kyber_lib.crypto_kem_keypair(pk.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
                                          sk.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)))
    if result != 0:
        raise RuntimeError("Keypair generation failed")
    return pk.tobytes(), sk.tobytes()

def encapsulate(public_key):
    ct = np.zeros(KYBER_CIPHERTEXTBYTES, dtype=np.uint8)
    ss = np.zeros(KYBER_SSBYTES, dtype=np.uint8)
    result = kyber_lib.crypto_kem_enc(ct.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
                                      ss.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
                                      np.frombuffer(public_key, dtype=np.uint8).ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)))
    if result != 0:
        raise RuntimeError("Encapsulation failed")
    return ct.tobytes(), ss.tobytes()

def decapsulate(ciphertext, private_key):
    ss = np.zeros(KYBER_SSBYTES, dtype=np.uint8)
    result = kyber_lib.crypto_kem_dec(ss.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
                                      np.frombuffer(ciphertext, dtype=np.uint8).ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
                                      np.frombuffer(private_key, dtype=np.uint8).ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)))
    if result != 0:
        raise RuntimeError("Decapsulation failed")
    return ss.tobytes()
