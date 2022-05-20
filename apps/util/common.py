import hashlib
from random import Random


def md5(text):
    # md5 32位加密
    m2 = hashlib.md5()
    m2.update(text.encode('utf8'))
    return m2.hexdigest()


def random_key(key_length=16):
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    return ''.join([chars[random.randint(0, length)] for _ in range(key_length)])


def allowed_photo(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_photo_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_file_EXTENSIONS
