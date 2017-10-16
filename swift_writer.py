import datetime

class SwiftWriter:
    def __init__(self, author='', company=''):
        self.author = author
        self.company = company

    def generate(self, model):
        with open(model.name + '.swift', 'w+') as f:
            self.__generate_header(f)
            f.write('import Foundation\n\n')
            f.write('public class ' + model.name + ' {\n')

            # Properties
            f.write('\n\t// MARK: - Properties\n\n')
            for prop in model.properties:
                data_type =  ('[' + prop.data_type.type_name + ']') if prop.is_list else prop.data_type.type_name
                f.write('\tvar ' + prop.name + ': ' + data_type + '?\n')

            # Initializers
            f.write('\n\t// MARK: - Initializers\n\n')
            f.write('\tpublic init(json: [String: Any]) {\n')
            for prop in model.properties:
                assignment = ''
                if prop.is_list:
                    if prop.data_type.is_primitive:
                        assignment = 'if let items = json["' + prop.json_field_name + '"] as? [' + prop.data_type.type_name + '] { ' + prop.name + ' = items.flatMap { $0 } }'
                    else:
                        assignment = 'if let items = json["' + prop.json_field_name + '"] as? [[String: Any]] { ' + prop.name + ' = items.map { ' + prop.data_type.type_name + '(json: $0) } }'
                else:
                    if prop.data_type.is_primitive:
                        assignment = prop.name + ' = ' + 'json["' + prop.json_field_name + '"] as? ' + prop.data_type.type_name
                    else:
                        assignment = 'if let item = json["' + prop.json_field_name + '"] as? [String: Any] { ' + prop.name + ' = ' + prop.data_type.type_name + '(json: item) }'
                f.write('\t\t' + assignment + '\n')
            f.write('\t}\n')

            # Methods
            f.write('\n\t// MARK: - Methods\n\n')
            f.write('\tpublic func toDictionary() -> [String: Any] {\n')
            f.write('\t\tvar dictionary: [String: Any] = [:]\n')
            for prop in model.properties:
                assignment = ''
                if prop.is_list:
                    if prop.data_type.is_primitive:
                        assignment = 'if let value = ' + prop.name + ' { dictionary["' + prop.json_field_name + '"] = value }\n'
                    else:
                        assignment = 'if let value = ' + prop.name + ' { dictionary["' + prop.json_field_name + '"] = value.map { $0.toDictionary() } }\n'
                else:
                    if prop.data_type.is_primitive:
                        assignment = 'if let value = ' + prop.name + ' { dictionary["' + prop.json_field_name + '"] = value }\n'
                    else:
                        assignment = 'if let value = ' + prop.name + ' { dictionary["' + prop.json_field_name + '"] = value.toDictionary() }\n'
                f.write('\t\t' + assignment) 
            f.write('\t\treturn dictionary\n')
            f.write('\t}\n')
            f.write('}\n')
    
    def __generate_header(self, model_file):
        now = datetime.datetime.now()
        formatted_date = now.strftime('%m/%d/%Y')
        model_file.write('//\n')
        model_file.write('// ' + model_file.name + '\n')
        model_file.write('//\n')
        model_file.write('// Created by ' + self.author + ' on ' + formatted_date + '.\n')
        model_file.write('// Copyright © ' + str(now.year) + ' ' + self.company + '. All rights reserved.\n\n')