import parser
import argparse
import jinja2
import constants as c

render_ctx = {}
parsed = parser.load_from_file('swagger.yaml')

templateLoader = jinja2.FileSystemLoader( searchpath="./")
templateEnv = jinja2.Environment( loader=templateLoader )
proto_template = "proto_template.proto"
template = templateEnv.get_template(proto_template)

### Rendering the protobuf
render_ctx.update(
    packagename='latch',
    parsed=parsed,
    verbs=c.OPERATION_CRUD_VERBS
)

print(template.render(render_ctx))
