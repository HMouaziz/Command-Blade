import hashlib


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
    elif hash_algorithm == "blake2b":
        return hashlib.blake2b(input_string.encode('utf-8')).hexdigest()
    elif hash_algorithm == "blake2s":
        return hashlib.blake2s(input_string.encode('utf-8')).hexdigest()
    else:
        return "Error"

