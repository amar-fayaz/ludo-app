class UserData():
    def __init__(self, username=None, host_ip=None):
        self.username = username
        self.host_ip = host_ip
    
    def get_username(self):
        return self.username

    def set_username(self, name):
        self.username = name

    def get_host_ip(self, ip):
        return self.host_ip

    def set_host_ip(self, ip):
        self.host_ip = ip