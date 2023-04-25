
class ClientCounter():
    client_count = 0

    def __init__(self):
        self.client_count = 0

    def add(self):
        self.client_count += 1

    def sub(self):
        self.client_count -= 1

    def get(self):
        return self.client_count

    def set(self, count):
        self.client_count = count

    def __str__(self):
        return str(self.client_count)

    def __repr__(self):
        return str(self.client_count)

    def __int__(self):
        return self.client_count


client_count = ClientCounter()
