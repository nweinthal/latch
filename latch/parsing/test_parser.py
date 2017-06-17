import unittest
import parser

class TestSwagger(unittest.TestCase):

  def test_parses_valid(self):
    yml = """
    swagger: '2.0'
    info:
      title: Bagels
      description: A type of bread
      version: 0.0.1
    paths:
      /flavors:
        get:
          summary: Bagels
          description: The available bagels
          parameters:
            - name: filter
              in: query
              description: type of bagels
              required: false
              type: string
          responses:
            '200':
              description: all the bagels
    """
    swagger = parser.load_from_string(yml)
    self.assertIsInstance(swagger, parser.Swagger)
    self.assertEqual(swagger.version, '2.0')
    self.assertTrue(hasattr(swagger, 'info'))
    self.assertTrue(hasattr(swagger, 'paths'))

  def test_missing_version_raises(self):
    yml = """
    info:
      title: Bagels
      description: A type of bread
      version: 0.0.1
    paths:
      /flavors:
        get:
          summary: Bagels
          description: The available bagels
          parameters:
            - name: filter
              in: query
              description: type of bagels
              required: false
              type: string
          responses:
            '200':
              description: all the bagels
    """
    with self.assertRaises(ValueError):
      swagger = parser.load_from_string(yml)

  def test_missing_info_raises(self):
    yml = """
    swagger: '2.0'
    paths:
      /flavors:
        get:
          summary: Bagels
          description: The available bagels
          parameters:
            - name: filter
              in: query
              description: type of bagels
              required: false
              type: string
          responses:
            '200':
              description: all the bagels
    """
    with self.assertRaises(ValueError):
      swagger = parser.load_from_string(yml)

  def test_missing_paths_raises(self):
    yml = """
    swagger: '2.0'
    info:
      title: Bagels
      description: A type of bread
      version: 0.0.1

    """
    with self.assertRaises(ValueError):
      swagger = parser.load_from_string(yml)

  def test_malformed_yaml_raises(self):
    yml  = """
    swagger 2.0
    """

    with self.assertRaises(TypeError):
      swagger = parser.load_from_string(yml)


class TestPaths(unittest.TestCase):

  def test_paths_construction(self):
    raw_paths = {"/dogs": {"get": "foo"}}
    paths = parser.Paths(raw_paths)
    self.assertIsInstance(paths.paths.get("dogs"), parser.PathItem)

  def test_paths_invalid_args(self):
    raw_paths = {"dogs": "foo"}
    with self.assertRaises(ValueError):
      paths = parser.Paths(raw_paths)

