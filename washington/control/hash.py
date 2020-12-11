import hashlib

BUFFER_SIZE = 65536 * 5


def get_signature(filepath):
    x = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if data:
                x.update(data)
            else:
                f.close()
                return x.hexdigest()
