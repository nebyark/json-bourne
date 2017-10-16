import json
import re
from enum import Enum

def is_primitive(data_type):
    return isinstance(data_type, str) or isinstance(data_type, int) or isinstance(data_type, float)

# Converts a string to either camelCase or PascalCase.
def convert_case(value, toPascal=False):
    if '_' in value:
        components = value.split('_')
    else:
        components = re.findall('[A-Z][a-z]*', value)
    if toPascal:
        if len(components) > 0:
            return ''.join(map(str.capitalize, components))
        else:
            return value.capitalize()
    else:
        if len(components) > 0:
            return components[0] + ''.join(map(str.capitalize, components[1:]))
        else:
            return value

class Model:
    def __init__(self, name='', properties=[]):
        self.properties = properties
        self.name = convert_case(name, toPascal=True)

class DataType:
    def __init__(self, type_name=''):
        self.is_primitive = True
        if 'class \'str\'' in type_name:
            self.type_name = 'String'
        elif 'class \'int\'' in type_name:
            self.type_name = 'Int'
        elif 'class \'float\'' in type_name:
            self.type_name = 'Float'            
        else:
            self.is_primitive = False
            self.type_name = convert_case(type_name, toPascal=True)

class Property:
    # Note: data_type can be a primitive (str, int, float), an array of primitives, or a custom type
    # Note: An array of primitives is denoted as <type>-list
    def __init__(self, name='', data_type=None, is_list=False):
        self.json_field_name = name
        self.name = convert_case(name, toPascal=False)
        self.data_type = DataType(type_name=data_type)
        self.is_list = is_list

class Parser:
    def __init__(self, root_name=''):
        self.root_name = root_name
        self.models = []

    # Parses a JSON dictionary.
    #
    # - Parameter root_json: A valid JSON dictionary. 
    # - Returns: A list of Models, each containing one or more Properties.
    def parse_json(self, root_json):
        self.parse_impl(root_json, self.root_name)
        return self.models

    # Parses a JSON file.
    #
    # - Parameter json_file: A file containing valid JSON dictionary. 
    # - Returns: A list of Models, each containing one or more Properties.
    def parse_json_file(self, json_file):
        root_json = json.load(open(json_file))
        return self.parse_json(root_json)

    # Recursive implementation function for parse_json().
    #
    # - Parameter root_json: The current root object.
    # - Parameter name: The current root object's name, essentially the current Class or Struct name.
    # - Returns: A list of Models, each containing one or more Properties.
    def parse_impl(self, root_json, name):
        properties = []
        for key, value in root_json.items():
            if isinstance(value, dict):
                # Keep traversing the object tree
                properties.append(Property(name=key, data_type=key))
                self.parse_impl(value, key)
            elif isinstance(value, list):
                # Check for primitives, otherwise keep traversing
                if is_primitive(value[0]):
                    list_type = str(type(value[0]))
                    properties.append(Property(name=key, data_type=list_type, is_list=True))
                else:
                    properties.append(Property(name=key, data_type=key, is_list=True))
                    self.parse_impl(value[0], key)
            else:
                # We've reached a leaf node
                properties.append(Property(name=key, data_type=str(type(value))))
        self.models.append(Model(name=name, properties=properties))
