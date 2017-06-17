from enum import Enum
"""
CURRENT FOR OpenAPI Spec 2.0
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md
"""
class SwaggerFields(Enum):
  SWAGGER = 'swagger'
  INFO = 'info'
  HOST = 'host'
  BASE_PATH = 'basePath'
  SCHEMES = 'schemes'
  CONSUMES = 'consumes'
  PRODUCES = 'produces'
  PATHS = 'paths'
  DEFINITIONS = 'definitions'
  PARAMETERS = 'parameters'
  RESPONSES = 'responses'
  SECURITY_DEFINITIONS = 'securityDefinitions'
  SECURITY = 'security'
  TAGS = 'tags'
  EXTERNAL_DOCS = 'externalDocs'


class InfoFields(Enum):
  TITLE = 'title'
  DESCRIPTION = 'description'
  TERMS_OF_SERVICE = 'termsOfService'
  CONTACT = 'contact'
  LICENSE = 'license'
  VERSION = 'version'


class PathItemFields(Enum):
  GET = 'get'
  PUT = 'put'
  POST = 'post'
  DELETE = 'delete'
  OPTIONS = 'options'
  HEAD = 'head'
  PATCH = 'patch'
  PARAMETERS = 'parameters'

PATH_ITEM_OPERATIONS = {
    PathItemFields.GET,
    PathItemFields.PUT,
    PathItemFields.POST,
    PathItemFields.DELETE,
    PathItemFields.OPTIONS,
    PathItemFields.HEAD,
    PathItemFields.PATCH
}

OPERATION_CRUD_VERBS = {
    PathItemFields.GET: "Get",
    PathItemFields.POST: "Create",
    PathItemFields.PUT: "Create",
    PathItemFields.PATCH: "Update",
    PathItemFields.DELETE: "Delete",
}

class OperationFields(Enum):
  TAGS = 'tags'
  SUMMARY = 'summary'
  DESCRIPTION = 'description'
  EXTERNAL_DOCS = 'externalDocs'
  OPERATION_ID = 'operationId'
  CONSUMES = 'consumes'
  PRODUCES = 'produces'
  PARAMETERS = 'parameters'
  RESPONSES = 'responses'
  SCHEMES = 'schemes'
  DEPRECATED = 'deprecated'
  SECURITY = 'security'

class ResponseFields(Enum):
  DESCRIPTION = 'description'
  SCHEMA = 'schema'
  HEADERS = 'headers'
  EXAMPLES = 'examples'

class DefinitionFields(Enum):
  FORMAT = 'format'
  TITLE = 'title'
  DESCRIPTION = 'description'
  DEFAULT = 'default'
  MULTIPLE_OF = 'multipleOf'
  MAXIMUM = 'maximum'
  EXCLUSIVE_MAXIMUM = 'exclusiveMaximum'
  MINIMUM = 'minimum'
  EXCLUSIVE_MINIMUM = 'exclusiveMinimum'
  PATTERN = 'pattern'
  MAX_ITEMS = 'maxItems'
  MIN_ITEMS = 'minItems'
  UNIQUE_ITEMS = 'uniqueItems'
  MAX_PROPERTIES = 'maxProperties'
  MIN_PROPERTIES = 'minProperties'
  REQUIRED = 'required'
  ENUM = 'enum'
  TYPE = 'type'
  ITEMS = 'items'
  ALL_OF = 'allOf'
  PROPERTIES = 'properties'
  ADDITIONAL_PROPERTIES = 'additionalProperties'
  DESCRIMINATOR = 'descriminator'
  READ_ONLY = 'readOnly'
  XML = 'xml'
  EXTERNAL_DOCS = 'externalDocs'
  EXAMPLE = 'example'

class ParameterFields(Enum):
  ADDITIONAL_PROPERTIES = 'additionalProperties'
  ALL_OF = 'allOf'
  BODY = 'body'
  DEFAULT = 'default'
  DESCRIMINATOR = 'descriminator'
  DESCRIPTION = 'description'
  ENUM = 'enum'
  EXAMPLE = 'example'
  EXCLUSIVE_MAXIMUM = 'exclusiveMaximum'
  EXCLUSIVE_MINIMUM = 'exclusiveMinimum'
  EXTERNAL_DOCS = 'externalDocs'
  FORMAT = 'format'
  IN = 'in'
  ITEMS = 'items'
  MAXIMUM = 'maximum'
  MAX_ITEMS = 'maxItems'
  MAX_PROPERTIES = 'maxProperties'
  MINIMUM = 'minimum'
  MIN_ITEMS = 'minItems'
  MIN_PROPERTIES = 'minProperties'
  MULTIPLE_OF = 'multipleOf'
  NAME = 'name'
  PATTERN = 'pattern'
  PROPERTIES = 'properties'
  READ_ONLY = 'readOnly'
  REQUIRED = 'required'
  SCHEMA = 'schema'
  TITLE = 'title'
  TYPE = 'type'
  UNIQUE_ITEMS = 'uniqueItems'
  XML = 'xml'

SWAGGER_TYPES = {
    "integer": int,
    "number": float,
    "string": str,
    "boolean": bool,
}

PROTOBUF_FORMATS = {
    "int32": "int32",
    "int64": "int64",
    "float": "float",
    "double": "double",
    "byte": "bytes",
}
