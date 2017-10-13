from parser import Parser
import sys, getopt

def usage():
    print('usage: json_derulo.py [-r <root class name>] [-f <file name>]')

def main(argv):
    # Get arguments
    try:
       opt_list, args = getopt.getopt(argv, 'r:f:', ['root=', 'file='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(420)

    json_file = None
    root_name = ''

    for opt, arg in opt_list:
        if opt in ('-r', '--root'):
            root_name = arg
        elif opt in ('-f', '--file'):
            json_file = arg
        else:
            assert False, 'Unhandled exception!'
    
    if json_file == None or root_name == '':
        print('Missing required arguments')
        usage()
        sys.exit(2)

    # Start parse
    p = Parser(root_name=root_name)
    models = p.parse_json_file(json_file)

    # TODO: Write files in specified language

if __name__ == '__main__':
    main(sys.argv[1:])