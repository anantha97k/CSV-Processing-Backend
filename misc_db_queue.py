from rq import Queue
from redis import Redis

# Tell RQ what Redis connection to use
redis_conn = Redis()

f = Queue(name="f", connection=redis_conn)  # no args implies the default queue

i = Queue(name="i", connection=redis_conn)  # no args implies the default queue
