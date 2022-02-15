from flask import request

class Util():
    def get_client_ip(self):
        return request.remote_addr