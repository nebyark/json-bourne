from parser import Parser
from swift_writer import SwiftWriter
import sys, getopt

def usage():
    print('usage: json_bourne.py [-r <root class name>] [-f <file name>] [-a <author name>] [-c <company name>] [-l <language name>]')
    print('Available language options: Swift')

def main(argv):
    # Get arguments
    try:
       opt_list, args = getopt.getopt(argv, 'r:f:a:c:l:', ['language=', 'root=', 'file=', 'author=', 'company='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(420)

    json_file = None
    root_name = 'BaseClass'
    author = 'JSON Bourne'
    company = ''
    language = None

    for opt, arg in opt_list:
        if opt in ('-r', '--root'):
            root_name = arg
        elif opt in ('-f', '--file'):
            json_file = arg
        elif opt in ('-a', '--author'):
            author = arg
        elif opt in ('-c', '--company'):
            company = arg
        elif opt in ('-l', '--language'):
            language = arg
        else:
            assert False, 'Unhandled exception!'
    
    if json_file == None or language == None or language == '':
        print('Missing required arguments')
        usage()
        sys.exit(2)

    # Start parse
    if language.lower() == 'swift':
        p = Parser(root_name=root_name)
        models = p.parse_json_file(json_file)
        swift_writer = SwiftWriter(author=author, company=company)
        for model in models:
            swift_writer.generate(model)
    else:
        print('Language not recognized')
    

if __name__ == '__main__':
    main(sys.argv[1:])