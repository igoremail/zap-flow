
import json
import redis
from typing import Any
from dataclasses import dataclass


username = 'default'
password = 'rjykAKrSGP1UJbRd5QNJhdkqgKfNzndu'
endpoint = 'redis-12394.c15.us-east-1-2.ec2.cloud.redislabs.com'
port = 12394

url_db = 'url_list'
data_db = 'zap_info'

@dataclass
class RedisDb:
    username : str = username
    password : str = password
    host     : Any = endpoint
    port     : int = port
    url_db   : str = url_db
    data_db  : str = data_db
    redis    : Any = None


    def connect(self, username=None, password=None, host=None, port=None):

        if username is not None:
            self.username = username

        if password is not None:
            self.password = password

        if host is not None:
            self.host = host

        if port is not None:
            self.port = port

        self.redis = redis.StrictRedis(host=self.host, port=self.port, username=self.username, password=self.password)


        if not self.redis.ping():
            raise Exception('Failed')


    def __del__(self):
        self.close()

    def close(self):
        self.redis.close()

    def flush_all(self):
        self.redis.flushall()

    def add_url(self, url):
        self.redis.hset(self.url_db, url, 0)

    def add_urls(self, urls):
        for url in urls:
            self.add_url(url)

    def del_url(self, urls):
        keys = self.redis.hgetall(self.url_db)
        for url in urls:
            if url in keys:
                self.redis.hdel(self.url_db, url)

    def add_data(self, data, key=None):
        if key is None:
            key = data['url']
        jd = json.dumps(data)
        self.redis.hset(self.data_db, key, jd)

    def add_data_list(self, data_list):
        for data in data_list:
            self.add_data(data)



def push_urls(urls):
    db = RedisDb()
    db.connect()
    db.add_urls(urls)
    pass


def push_data(data):
    db = RedisDb()
    db.connect()
    db.add_data_list(data)
    pass