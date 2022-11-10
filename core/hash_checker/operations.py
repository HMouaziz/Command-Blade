import hashlib
import sys


def hash_string(hash_algorithm, input_string):
    if hash_algorithm == "MD5":
        return hashlib.md5(input_string.encode('utf-8')).hexdigest()
    elif hash_algorithm == "SHA1":
        return hashlib.sha1(input_string.encode('utf-8')).hexdigest()
    elif hash_algorithm == "SHA224":
        return hashlib.sha224(input_string.encode('utf-8')).hexdigest()
    elif hash_algorithm == "SHA256":
        return hashlib.sha256(input_string.encode('utf-8')).hexdigest()
    elif hash_algorithm == "SHA384":
        return hashlib.sha384(input_string.encode('utf-8')).hexdigest()
    elif hash_algorithm == "SHA512":
        return hashlib.sha512(input_string.encode('utf-8')).hexdigest()
    elif hash_algorithm == "BLAKE2B":
        return hashlib.blake2b(input_string.encode('utf-8')).hexdigest()
    elif hash_algorithm == "BLAKE2S":
        return hashlib.blake2s(input_string.encode('utf-8')).hexdigest()
    else:
        return "Error"


def hash_file(hash_algorithm, filepath, buffer_size=65536):
    hash_algorithm_function = getattr(hashlib, hash_algorithm.lower())
    file = hash_algorithm_function()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            file.update(data)
    hashed_file = file
    return hashed_file
