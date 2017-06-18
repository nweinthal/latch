import argparse
import jinja2

from latch.parsing import constants as c
from latch.parsing import parser

def swagger_to_protobuf(filename):
  render_ctx = {}
  parsed = parser.load_from_file(filename)

  templateLoader = jinja2.PackageLoader('latch', 'data')
  templateEnv = jinja2.Environment( loader=templateLoader )
  proto_template = "proto_template.proto"
  template = templateEnv.get_template(proto_template)

  ### Rendering the protobuf
  render_ctx.update(
      packagename='latch',
      parsed=parsed,
      verbs=c.OPERATION_CRUD_VERBS
  )
  return template.render(render_ctx)
