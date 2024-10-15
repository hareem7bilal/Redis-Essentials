import redis
import time

def connect_to_redis(max_retries=3, retry_delay=2):
    for attempt in range(max_retries):
        try:
            redisObj = redis.Redis(host='localhost', port=6379, db=0)
            redisObj.ping()  # Test the connection
            print("Successfully connected to Redis")
            return redisObj
        except redis.exceptions.ConnectionError as e:
            print(f"Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Could not connect to Redis.")
                raise

redisObj = connect_to_redis()
pipeObj = redisObj.pipeline()

pipeObj.set("Name", "Jack")
pipeObj.set("a", 10)
pipeObj.set("b", 10)
pipeObj.set("p", 10)
pipeObj.set("q", 10)
pipeObj.set("n", 10)

pipeObj.execute()

print("\n----------------------Original Values")
print("Name: ", redisObj.get("Name"))
print("a: ", redisObj.get("a"))
print("b: ", redisObj.get("b"))
print("p: ", redisObj.get("p"))
print("q: ", redisObj.get("q"))
print("n: ", redisObj.get("n"))

pipeObj.append("Name", " Jonas")
pipeObj.incr("a")
pipeObj.incrby("b",3)
pipeObj.incrbyfloat("p",0.5)
pipeObj.delete("q")

print("\n----------------------Updating")

pipeObj.execute()

print("\n----------------------Updated Values")

print("APPEND Name Jonas: ", redisObj.get("Name"))
print("INCR a: ", redisObj.get("a"))
print("INCRBY b 3: ", redisObj.get("b"))
print("INCRBYFLOAT p 0.5: ", redisObj.get("p"))
print("DELETE q: ", redisObj.get("q"))
print("(No op) n: ", redisObj.get("n"))

