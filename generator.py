

from redis import StrictRedis
import warnings

BUFFER = 20

class Generator(object):
    def __init__(self, start_from=1, key=None, connection=None):
        if key is None:
            raise Exception('Param Key cannot be null')
        if not isinstance(connection, StrictRedis):
            raise Exception('connection should be an object of StrictRedis')
        self.connection = connection
        self.key = key
        if self.connection.exists(key):
            current_id = self.connection.lindex(key, (connection.llen(key)-1))
            if current_id is not None:
                if int(current_id) > start_from and start_from > 1:
                    raise Exception("Current sequence of id "+str(current_id)+" cannot be greated than start_of.")

            # Clearing old values as new start_from passed for the key
            self.connection.delete(key)

            # Regenerating buffer ids
            self.__addtolist(start_from, key)
        else:
            # Generating buffer ids
            self.__addtolist(start_from, key)


    def __addtolist(self, start_from, key):
        for x in range(start_from, (start_from + BUFFER)):
            self.connection.rpush(key, x)


    def getId(self):
        unique_id = self.connection.lpop(self.key)
        self.connection.rpush(self.key, (int(unique_id) + BUFFER))
        return unique_id
