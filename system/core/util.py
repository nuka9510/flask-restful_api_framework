from flask import request

class Util():
    def __init__(self):
        pass

    def get_client_ip(self):
        return request.remote_addr