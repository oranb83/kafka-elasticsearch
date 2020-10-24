# NOTE:
# I use a weak single redis cluster locally with bad performance, due to networking container.
# I chose to do it only beacuse that way I can control all testing envrionments instead of
# instructing how to install redis (with better performance) and pay for it in bugs per OS and
# redis versions.
# In real life I'll use muitiple redis clusters managed by redislabs on AWS based on past
# experience. But even locally if I'll set serveral clusters I could just write every word with
# redis pipeline (batch transaction) directly to redis and it whould have been much faster and
# simpler than creating an in memory logic to count words and save to redis when a condition is met.

import redis


class Redis:
    """
    This class handles redis connection and IO.
    """
    redis_client = redis.Redis(host='redis', port=6379)

    def save(self, counter):
        """
        This method saves data into redis and clears the counter so the data will not be added
        again as duplicated data.

        @type counter: collections.Counter
        @param counter: dict => {word: num_of_appearance}
        """
        # TODO: need to add try except and retries in case of connection issues, not a problem
        #       when connected to a single local redis cluster.
        with self.redis_client.pipeline() as pipe:
            for key, value in counter.items():
                pipe.incrby(key, value)
            pipe.execute()
        counter.clear()

    def get(self, key):
        """
        This method gets a key from redis as return it's value as int.

        @type key: str
        @param key: key=word to search.
        @rtype: int
        @return: word search num of appearance >= 0 (uint)
        """
        # Assumption: if a key is missing we will return 0
        return int(self.redis_client.get(key) or 0)
