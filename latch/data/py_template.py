import asyncio
import json
import redis
import urllib.parse
import aiohttp_cors

from aiohttp import web
from collections import namedtuple
from google.protobuf.json_format import *

from api.v1.proto import api_pb2 as api

db = redis.StrictRedis('localhost', 6379)

{% for definition in parsed.definitions %}
async def {{['list', definition, 'Handler']|join('')}}(request):
  {{definition|lower}}_set = db.smembers('{{definition}}')
  decoded = []
  for bytestring in {{definition|lower}}_set:
    msg = api.{{definition}}()
    msg.ParseFromString(bytestring)
    decoded.append(MessageToDict(msg))
  return web.Response(text=json.dumps(decoded))

async def {{['get', definition, 'Handler']|join('')}}(request):
  return web.Response(text="Hello, world")

async def {{['create', definition, 'Handler']|join('')}}(request):
  data = await request.json()
  item = api.{{definition}}(**data)
  db.sadd('{{definition}}', item.SerializeToString())
  return web.json_response(MessageToJson(item))

async def {{['update', definition, 'Handler']|join('')}}(request):
  return web.Response(text="Hello, world")

async def {{['delete', definition, 'Handler']|join('')}}(request):
  return web.Response(text="Hello, world")

async def {{['options', definition, 'Handler']|join('')}}(request):
  return web.Response(status=204)
{% endfor %}

if __name__ == '__main__':
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

  ##OPTIONS
  #options_resource = cors.add(
  #    app.router.add_resource({{definition|lower}}_options_url,
  #    name='Options{{definition}}'))
  #cors.add(options_resource.add_route('OPTIONS',
  #    options{{definition}}Handler))

  {% endfor %}
  web.run_app(app, port=8888)
