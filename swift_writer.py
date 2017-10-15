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
            f.write('\n\t// MARK: - Properties\n\n')
            for prop in model.properties:
                f.write('\tvar ' + prop.name + ': ' + str(prop.data_type) + '?\n')
            f.write('}\n')
    
    def __generate_header(self, model_file):
        now = datetime.datetime.now()
        formatted_date = now.strftime('%m/%d/%Y')
        model_file.write('//\n')
        model_file.write('// ' + model_file.name + '\n')
        model_file.write('//\n')
        model_file.write('// Created by ' + self.author + ' on ' + formatted_date + '.\n')
        model_file.write('// Copyright © ' + str(now.year) + ' ' + self.company + '. All rights reserved.\n\n')