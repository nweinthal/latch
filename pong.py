import asyncio
import redis
import time

r = redis.StrictRedis(host="localhost", port=6379)

class DopeySubscriber:
  def __init__(self, topic):
    self.authority = r.pubsub()
    self.authority.subscribe(topic)

  def work(self, item):
    print(item['channel'], ":", item['data'])
    time.sleep(1)
    print("pong")
    r.publish("response:index", "pong")

  def run(self, loop):
    print("subscribing")
    for item in self.authority.listen():
      if item.get('DATA') == "KILL":
        self.authority.unsubscribe()
        print("unsubscribed")
        loop.stop()
        break
      else:
        self.work(item)

subber = DopeySubscriber("index")

try:
  loop = asyncio.get_event_loop()
  loop.call_soon(subber.run, loop)
  loop.run_forever()

finally:
  loop.close()
