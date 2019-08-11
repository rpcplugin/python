
class Handshake(object):
    cookie_key = None
    cookie_value = None

    def __init__(self, cookie_key, cookie_value):
        self.cookie_key = cookie_key
        self.cookie_value = cookie_value


__all__ = [
    'Handshake'
]
