

import redis
import warnings

connection = redis.StrictRedis(host='0.0.0.0', port=6379,db=7)

BUFFER = 20

class Generator(object):
    def __init__(self, start_from=1, key=None):
        if key is None:
            raise Exception('Param Key cannot be null')
        self.key = key
        if connection.exists(key):
            current_id = connection.lindex(key, (connection.llen(key)-1))
            if current_id is not None:
                if int(current_id) > start_from and start_from > 1:
                    raise Exception("Current sequence of id "+str(current_id)+" cannot be greated than start_of.")

            # Clearing old values as new start_from passed for the key
            connection.delete(key)

            # Regenerating buffer ids
            self.__addtolist(start_from, key)
        else:
            # Generating buffer ids
            self.__addtolist(start_from, key)


    def __addtolist(self, start_from, key):
        for x in range(start_from, (start_from + BUFFER)):
            connection.rpush(key, x)


    def getId(self):
        unique_id = connection.lpop(self.key)
        connection.rpush(self.key, (int(unique_id) + BUFFER))
        return unique_id
