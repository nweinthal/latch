import asyncio
from aiohttp import web
import redis
import aioredis

async def release_latch(subscriber):
  res = await subscriber.subscribe('response:index')
  print("Subscribed")
  channel = res[0]
  async for msg in channel.iter(encoding='utf-8'):
    print("Got Message:", msg)
    return msg

async def set_latch(request):
  controller = request.app.get('redis_controller')
  publisher = controller[0]
  subscriber = controller[1] #TODO named tuples r cool
  await publisher.publish('index', "ping")
  msg = await asyncio.wait_for(release_latch(subscriber), 5.0)
  return web.Response(text=msg)

async def initialize_redis(app):
  publisher = await aioredis.create_redis(('localhost', 6379), loop=app.loop)
  subscriber = await aioredis.create_redis(('localhost', 6379), loop=app.loop)
  await publisher.publish("index", "hello")
  controller = (publisher, subscriber)
  app['redis_controller'] = controller

async def cleanup(app):
  (c.quit() for c in app['redis_controller'])

if __name__ == '__main__':
  app = web.Application()
  app.on_startup.append(initialize_redis)
  app.router.add_get('/', set_latch)
  app.on_cleanup.append(cleanup)
  web.run_app(app)
