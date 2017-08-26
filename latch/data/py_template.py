import aiohttp_cors
import aioredis
import asyncio
import copy
import json
import redis
import urllib.parse

from aiohttp import web
from collections import namedtuple, defaultdict
from google.protobuf.json_format import *

from api.v1.proto import api_pb2 as api


request_channels = defaultdict(dict)
response_channels = defaultdict(dict)
response_subscriptions = defaultdict(dict)
resource_operations = ['list', 'get', 'create', 'update', 'delete']

{% for definition in parsed.definitions %}

for operation in resource_operations:
  # TODO - in settings, allow the top level resource designator to be set
  # instead of hardcoded 'latch'
  uri_path = ('latch', operation, '{{definition|lower}}')

  # a request uri will look like 'latch:get:resource:request', e.g.

  request_resource_uri = ':'.join(uri_path + ('request',))
  response_resource_uri = ':'.join(uri_path + ('response',))
  print(response_resource_uri)
  request_channels[operation]['{{definition|lower}}'] = request_resource_uri
  response_subscriptions[operation]['{{definition|lower}}'] = None
  response_channels[operation]['{{definition|lower}}'] = response_resource_uri


async def {{['list', definition, 'Handler']|join('')}}(request):
  '''
  {{definition|lower}}_set = db.smembers('{{definition}}')
  decoded = []
  for bytestring in {{definition|lower}}_set:
    msg = api.{{definition}}()
    msg.ParseFromString(bytestring)
    decoded.append(MessageToDict(msg))
  return web.Response(text=json.dumps(decoded))
  '''
  channel = app['request_channels']['list']['{{definition|lower}}']
  request.app['publisher'].publish(channel, "list me!")
  return web.Response(text="Hello, world")

async def {{['get', definition, 'Handler']|join('')}}(request):
  channel = app['request_channels']['get']['{{definition|lower}}']
  print("Got request, publishing to channel", channel)
  request.app['publisher'].publish(channel, "get me!")
  return web.Response(text="Hello, world")

async def {{['create', definition, 'Handler']|join('')}}(request):
  data = await request.json()
  item = api.{{definition}}(**data)
  db.sadd('{{definition}}', item.SerializeToString())
  return web.json_response(MessageToJson(item))

async def {{['update', definition, 'Handler']|join('')}}(request):
  return web.Response(text="Hello, world")

async def {{['delete', definition, 'Handler']|join('')}}(request):
  data = await request.json()
  return web.Response(text="Hello, world")

async def {{['options', definition, 'Handler']|join('')}}(request):
  return web.Response(status=204)
{% endfor %}


async def engage_redis(app):
  publisher = await aioredis.create_redis(('localhost', 6379))
  subscriber = await aioredis.create_redis(('localhost', 6379))
  app['publisher'] = publisher
  app['subscriber'] = subscriber

  # this copy isn't thread safe if that causes problems down the line
  app['request_channels'] = copy.deepcopy(request_channels)
  app['response_subscriptions'] = copy.deepcopy(response_subscriptions)
  uris = []
  for operation in response_channels:
    for channel in response_channels.get(operation):
      uris.append(response_channels.get(operation).get(channel))

  app['active_channels'] = uris
  subscriptions = await subscriber.subscribe(*uris)

  # TODO this depends on matching order between uris and subscriptions,
  # which I'd rather it not

  for i, uri in enumerate(uris):
    try:
      app_name, verb, resource, response_str = uri.split(':')
    except ValueError:
      raise ValueError(uris)
    app['response_subscriptions'][verb][resource] = subscriptions[i]

  # TODO better logging
  print("Connections active on redis server")

async def start_background_tasks(app):
  print("Connecting to redis server")
  app['redis_task'] = app.loop.create_task(engage_redis(app))

async def cleanup_background_tasks(app):
  print("cleaning up redis")
  await app['subscriber'].unsubscribe(*app['active_channels'])
  await app['publisher'].quit()
  await app['subscriber'].quit()

app = web.Application()
cors = aiohttp_cors.setup(app, defaults={
  "*": aiohttp_cors.ResourceOptions(
     allow_credentials=True,
     allow_methods="*",
     expose_headers="*",
     allow_headers="*")
})
{% for definition in parsed.definitions %}
resource_root = urllib.parse.urljoin('{{parsed.basePath}}/',
    '{{definition|lower}}s')
{{definition|lower}}_list_url = resource_root
{{definition|lower}}_get_url = resource_root + '/{id}'
{{definition|lower}}_create_url = resource_root
{{definition|lower}}_delete_url = resource_root + '/{id}'
{{definition|lower}}_update_url = resource_root + '/{id}'
{{definition|lower}}_options_url = resource_root
# LIST
list_resource = cors.add(
  app.router.add_resource({{definition|lower}}_list_url,
    name='List{{definition}}s'))
cors.add(list_resource.add_route('GET', list{{definition}}Handler))

# GET
get_resource = cors.add(
  app.router.add_resource({{definition|lower}}_get_url,
    name='Get{{definition}}'))
cors.add(get_resource.add_route('GET', get{{definition}}Handler))

# CREATE
create_resource = cors.add(
  app.router.add_resource({{definition|lower}}_create_url,
    name='Create{{definition}}'))
cors.add(create_resource.add_route('POST', create{{definition}}Handler))

# UPDATE
update_resource = cors.add(
  app.router.add_resource({{definition|lower}}_update_url,
    name='Update{{definition}}'))
cors.add(update_resource.add_route('PATCH',
    update{{definition}}Handler))

# DELETE
delete_resource = cors.add(
  app.router.add_resource({{definition|lower}}_delete_url,
    name='Delete{{definition}}'))
cors.add(delete_resource.add_route('DELETE',
    delete{{definition}}Handler))

{% endfor %}

app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)
web.run_app(app, port=8888)
