from .redis_store import Storage


class Store:
    def __init__(self):
        self.store = Storage()
    
    def set(self, *args):
        if len(*args) > 2:
            options = args[0]
            if options[2] == b"px":
                key = options[0]
                key = key.decode("utf-8")
                value = options[1]
                expiry = options[3]
                expiry = expiry.decode("utf-8")
                expiryInMilliseconds = int(expiry)
                self.store.set_with_expiry(
                    key=key,
                    value=value,
                    expiry=expiryInMilliseconds
                )
                return True
            else:
                return False
        elif len(*args) == 2:
            key, value = args[0]
            key = key.decode('utf-8')
            self.store.set(key, value)
            return True
        return False

    def get(self, *args):
        if len(*args) == 1:
            key = args[0][0]
            key = key.decode('utf-8')
            value, found = self.store.get(key)
            if found:
                return value
        return None
