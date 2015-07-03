from uuid import uuid4
from base64 import b64encode


class ApnProxyConfig(object):
    description = 'Custom Apn Proxy Profile'
    organization = 'Realityone'

    def __init__(self, proxy_ip, port, name='Apn Proxy Config', username=None, password=None):
        self.name = name
        self.proxy_ip = proxy_ip
        self.port = port
        self.username = username or ''
        self.password = password or ''

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = b64encode(value).strip()

    @classmethod
    def _uuid(cls):
        return str(uuid4()).upper()

    @property
    def config_uid(self):
        return self._uuid()

    @property
    def file_uuid(self):
        return self._uuid()


if __name__ == '__main__':
    apn = ApnProxyConfig('127.0.0.1', 1234)
    print apn.password, apn.file_uuid, apn.config_uid