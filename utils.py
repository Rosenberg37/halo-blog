import hashlib
from random import Random


def md5(text):
    # md5 32位加密
    m2 = hashlib.md5()
    m2.update(text.encode('utf8'))
    return m2.hexdigest()


def verity_password(origin_password, password):
    new_password = md5(origin_password)
    return password == new_password


def random_key(key_length=16):
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    return ''.join([chars[random.randint(0, length)] for _ in range(key_length)])
