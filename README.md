# json-bourne
![alt text](https://i.imgur.com/8LnmYEn.jpg)
The CIA's most dangerous JSON payload to model file tool.

## Requirements
* Python 3.x
* A valid JSON payload

## Usage
Once more model writers are added to this project, I'll upload a unix binary if Jason lets me. For now though, to generate your model files, run the following:

```python json_bourne.py -l <language name> -r <root class name> -a <author name> -c <company name> -f <relative path to JSON file>```

ex:

```python json_bourne.py -l Swift -r MyLittleIdentity -a 'JSON Bourne' -c 'CIA' -f my_little_payload.json```

## Arguments
* -r, --root (optional): The name of the root class or top level of the JSON payload tree.
* -a, --author (optional): The author name to be inserted in the generated header comment. Typically your name.
* -c, --company (optional): The company name to be inserted in the generated header comment. Typically your company name.
* -f, --file (required): The name of the file, including the extension.
* -l, --language (required): The language to generate the model file in.

## Available languages
* Swift 3/4
