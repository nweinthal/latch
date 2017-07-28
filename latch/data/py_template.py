import asyncio
import json
import redis
import urllib.parse

from aiohttp import web
from collections import namedtuple
from google.protobuf.json_format import *

from api.v1.proto import api_pb2 as api

db = redis.StrictRedis('localhost', 6379)

{% for definition in parsed.definitions %}
async def {{['list', definition, 'Handler']|join('')}}(request):
  {{defintion|lower}}_set = db.smembers('{{definition}}')
  decoded = set(MessageToDict(i) for i in {{definition|lower}}_set)
  return web.Response(text=json.dumps(decoded))

async def {{['get', definition, 'Handler']|join('')}}(request):
  return web.Response(text="Hello, world")

async def {{['create', definition, 'Handler']|join('')}}(request):
  data = await request.json()
  item = api.{{definition}}(**data)
  db.sadd('{{definition}}', item)
  return web.json_response(MessageToJson(item))

async def {{['update', definition, 'Handler']|join('')}}(request):
  return web.Response(text="Hello, world")

async def {{['delete', definition, 'Handler']|join('')}}(request):
  return web.Response(text="Hello, world")
{% endfor %}

if __name__ == '__main__':
  app = web.Application()
  {% for definition in parsed.definitions %}
  resource_root = urllib.parse.urljoin('{{parsed.basePath}}/',
      '{{definition|lower}}s')
  {{definition|lower}}_list_url = resource_root
  {{definition|lower}}_get_url = resource_root + '/{id}'
  {{definition|lower}}_create_url = resource_root
  {{definition|lower}}_delete_url = resource_root + '/{id}'
  {{definition|lower}}_update_url = resource_root + '/{id}'

  # LIST
  list_resource = app.router.add_resource({{definition|lower}}_list_url,
      name='List{{definition}}s')
  list_route = list_resource.add_route('GET', list{{definition}}Handler)

  # GET
  get_resource = app.router.add_resource({{definition|lower}}_get_url,
      name='Get{{definition}}')
  get_route = get_resource.add_route('GET', get{{definition}}Handler)

  # CREATE
  create_resource = app.router.add_resource({{definition|lower}}_create_url,
      name='Create{{definition}}')
  create_route = create_resource.add_route('POST', create{{definition}}Handler)

  # UPDATE
  update_resource = app.router.add_resource({{definition|lower}}_update_url,
      name='Update{{definition}}')
  update_route = update_resource.add_route('PATCH',
      update{{definition}}Handler)

  # DELETE
  delete_resource = app.router.add_resource({{definition|lower}}_delete_url,
      name='Delete{{definition}}')
  delete_route = delete_resource.add_route('DELETE',
      delete{{definition}}Handler)
  {% endfor %}
  web.run_app(app, port=8888)
