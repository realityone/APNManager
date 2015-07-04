try:
    import cPickle as pickle
except ImportError:
    import pickle
import redis
import logging
from hashlib import md5


class NoSuchPrifile(Exception):
    pass


class RedisDB(object):
    EXPIRE = 7 * 24 * 60 * 60

    def __init__(self, host='localhost', port=6379, db=0):
        try:
            self.client = redis.StrictRedis(host=host, port=port, db=db,
                                            socket_timeout=3,
                                            socket_connect_timeout=3)
            self.client.ping()
        except redis.ConnectionError as e:
            logging.error(e)
            self.client = None

    def _prefix(self, code):
        return 'apnproxy:%s' % code

    def _genrate_code(self, obj):
        data = pickle.dumps(obj)
        code = md5(data).hexdigest()
        return code, data

    def save_profile(self, config):
        code, data = self._genrate_code(config)
        full_code = self._prefix(code)
        self.client.set(full_code, data)
        self.client.expire(full_code, self.EXPIRE)
        return code

    def get_profile(self, code):
        full_code = self._prefix(code)
        data = self.client.get(full_code)
        if data is None:
            raise NoSuchPrifile('No such profile')
        else:
            return pickle.loads(data)