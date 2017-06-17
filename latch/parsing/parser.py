import yaml

from .constants import *
from jsonschema import validate

class Swagger:

  def __init__(self, *args, **kwargs):
    # TODO nice errors
    remapped = {SwaggerFields(k): kwargs[k] for k in kwargs}

    # Should fail absent required fields
    try:
      self.version = remapped.pop(SwaggerFields.SWAGGER)
      self.info = remapped.pop(SwaggerFields.INFO)
      self.paths = Paths(remapped.pop(SwaggerFields.PATHS))

    except KeyError as e:
      raise ValueError("Swagger minimally requires fields: {}, {}, {}".format(
        SwaggerFields.SWAGGER.value,
        SwaggerFields.INFO.value,
        SwaggerFields.PATHS.value))

    # TODO Make classes for the other guys, as needed

    self.definitions = Definitions(remapped.pop(SwaggerFields.DEFINITIONS))

    self.__dict__.update({k.value: remapped[k] for k in remapped})

class Paths(dict):

  def __init__(self, path_dict):
    if not all(path.startswith('/') for path in path_dict):
      raise ValueError("All paths must start with '/'")
    super().__init__({p.strip('/'): PathItem(**path_dict[p])\
        for p in path_dict})

class PathItem:

  def __init__(self, *args, **kwargs):
    remapped = {PathItemFields(k): kwargs[k] for k in kwargs}
    self.supported_operations = PATH_ITEM_OPERATIONS.intersection(remapped)
    for op in self.supported_operations:
      x = remapped.pop(op)
      self.__dict__.update({op.value: Operation(**x)})
    self.__dict__.update({k.value: Operation(**remapped[k]) for k in remapped})

  def __repr__(self):
    return "Path Operations: {}".format(self.supported_operations)

class Operation:

  def __init__(self, *args, **kwargs):
    remapped = {OperationFields(k): kwargs[k] for k in kwargs}
    self.responses = Responses(remapped.pop(OperationFields.RESPONSES))
    self.__dict__.update({k.value: remapped[k] for k in remapped})
    self.parameters = [Parameter(**p) for p in self.parameters]

class Responses:

  def __init__(self, resp_dict):
    self.responses = {r: Response(**i) for r, i in resp_dict.items()}

class Response:

  def __init__(self, *args, **kwargs):
    remapped = {ResponseFields(k): kwargs[k] for k in kwargs}
    self.description = remapped.pop(ResponseFields.DESCRIPTION)
    self.__dict__.update({k.value: remapped[k] for k in remapped})

class Definitions(dict):

  def __init__(self, def_dict):
    super().__init__({d: Definition(**def_dict[d]) for d in def_dict})

class Definition:
  """
  This class is quite important.  It ought to be an extension of JSON schema, but
  it ends up being the class that details all of the proto fields
  """
  def __init__(self, *args, **kwargs):
    remapped = _remap(kwargs, DefinitionFields)
    self.properties = {}
    _props = remapped.pop(DefinitionFields.PROPERTIES)
    for property_name in _props:
      self.properties.update({property_name: Property(
        _remap(_props.get(property_name), DefinitionFields))})

    self.__dict__.update({k.value: remapped[k] for k in remapped})

class Property:

  def __init__(self, definition):
    self.type = definition.pop(DefinitionFields.TYPE)
    self.format = definition.pop(DefinitionFields.FORMAT, None)

    # TODO more elegantly handle unspecified formats
    if self.format is None:
      self.format = "int64" if self.type == "integer"\
               else "float" if self.type == "number"\
               else None
    if self.type =="array":
      try:
        self.items = definition.pop(DefinitionFields.ITEMS)
      except KeyError:
        raise ValueError("Array definitions must have accompanying item")
      self.format = "repeated"
    self.__dict__.update({k.value: definition[k] for k in definition})

class Parameter(Property):
  def __init__(self, *args, **kwargs):
    self.name = kwargs.pop(ParameterFields.NAME.value)
    self.in_type = ParameterInTypes(kwargs.pop(ParameterFields.IN.value))
    remapped = _remap(kwargs, ParameterFields)
    if self.in_type is not ParameterInTypes.BODY:
      remapped = _remap(kwargs, DefinitionFields)
      super().__init__(remapped)
    else:
      self.schema = remapped.pop(ParameterFields.SCHEMA)
      if REFERENCE in self.schema:
        path = self.schema.get(REFERENCE).split('/')
        # TODO - somehow we might want to traverse back to definitions to assert
        # existence of the referent object?
        self.format = path[-1]
      else:
        # TODO - figure out how to get non-referencing schemas working
        raise NotImplementedError


def _remap(dict_like, enumeration):
  return {enumeration(k): dict_like[k] for k in dict_like}

def load_from_string(string):
  raw = yaml.load(string)
  return Swagger(**raw)

def load_from_file(filename):
  with open(filename, 'r') as stream:
    raw = yaml.load(stream)
    return Swagger(**raw)

