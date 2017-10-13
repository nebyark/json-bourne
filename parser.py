import json

def is_primitive(data_type):
    return isinstance(data_type, str) or isinstance(data_type, int) or isinstance(data_type, float)

class Model:
    # Note: This is essentially the class or struct that is to be written into whatever language.
    def __init__(self, name='', properties=[]):
        self.properties = properties
        self.name = name
        for prop in properties:
            print(prop.name + ': ' + str(prop.data_type))

class Property:
    # Note: data_type can be a primitive (str, int, float), an array of primitives, or a custom type
    # Note: An array of primitives is denoted as <type>-list
    def __init__(self, name='', data_type=None):
        self.name = name
        self.data_type = data_type

class Parser:

    def __init__(self, root_name=''):
        self.root_name = root_name
        self.models = []

    # Recursively parses a JSON dictionary.
    #
    # - Parameter root_json: A valid JSON dictionary. 
    # - Returns: A list of Models, each containing one or more Properties.
    def parse_json(self, root_json):
        self.parse_helper(root_json, self.root_name)
        return self.models

    # Recursively parses a JSON dictionary.
    #
    # - Parameter json_file: A file containing valid JSON dictionary. 
    # - Returns: A list of Models, each containing one or more Properties.
    def parse_json_file(self, json_file):
        root_json = json.load(open(json_file))
        return self.parse_json(root_json)

    # Recursive helper function for parse_json*
    #
    # - Parameter root_json: The current root object.
    # - Parameter name: The current root object's name, essentially the current Class or Struct name.
    # - Returns: A list of Models, each containing one or more Properties.
    def parse_helper(self, root_json, name):
        properties = []
        for key, value in root_json.items():
            if isinstance(value, dict):
                # Keep traversing the object tree
                properties.append(Property(name=key, data_type=key))
                self.parse_helper(value, key)
            elif isinstance(value, list):
                # Check for primitives, otherwise keep traversing
                if is_primitive(value[0]):
                    list_type = str(type(value[0])) + '-list'
                    properties.append(Property(name=key, data_type=list_type))
                else:
                    properties.append(Property(name=key, data_type=key))
                    self.parse_helper(value[0], key)
            else:
                # Essentially child leaves of the object tree
                properties.append(Property(name=key, data_type=type(value)))
           
        self.models.append(Model(name=name, properties=properties))
