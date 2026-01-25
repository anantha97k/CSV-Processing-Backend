from rq import Queue
from redis import Redis

# Tell RQ what Redis connection to use
redis_conn = Redis()
q = Queue(name='q', connection=redis_conn)  # no args implies the default queue



