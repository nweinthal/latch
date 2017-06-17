from aiohttp import web
import redis
import aioredis

controller = aioredis.create_redis(('localhost', 6379))

async def index_latch:
  ps = controller.pubsub()
  ps.subscribe("index")
  for item in ps.listen():


async def index(request):
  controller.publish("index", "ping")
  response = await index_latch()
  if response == "pong":
    return web.Response(text="Hello, world")

def initialize_routes(app):
  app.router.add_get('/', index)
  asyncio.ensure_future(index)
