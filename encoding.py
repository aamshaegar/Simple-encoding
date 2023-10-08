import json
import sys
import os

__name__ = "__main__"


def open_and_check(file_path):
    """
        Open a file and read all lines.
        - Throw FileNotFoundError if file not exists
        - Throw ValueError if file is void
        - param "file_path": path of a file
    """

    try:
        file = open(file_path, "r", encoding='utf8')
    except FileNotFoundError:
        print("Error! File not found...")
        exit()

    lines = file.readlines()
    if lines == []:
        raise ValueError("Error, void file in input!")

    file.close()
    return lines



def get_json_file(path_json:str, encoding:str = 'utf-8'):
  """Get a judgments file at the specified path

  Args:
      path_json (str): the path of the file.
      encoding (str, optional): an encoding type. Defaults to 'utf-8'.

  Returns:
      dict: the judgments file retrieved
  """

  with open(path_json, 'r', encoding=encoding) as f:
    json_loaded = json.load(f)
    return json_loaded



def save_json_file(path_json:str, json_obj:dict, encoding:str= 'utf-8'):
  """Export a judgments file

  Args:
      path_json (str): the export path of the judgments file
      json_obj (dict): a dictionary
      encoding (str, optional): an encoding type. Defaults to 'utf-8'.
  """
  try:
    with open(path_json, "w", encoding=encoding) as file:
        json.dump(fp=file, obj=json_obj,indent=4,  ensure_ascii=False)
  except Exception:
    print("Incorrect encoding or not a dictionary!")



def document_preprocessing(document):
    
    # FOR FURTHER IMPROVING
    # ACTUALLY NOT USED
    #document = [line.replace('\n','') for line in document if line != '\n']
    return document



def splitting_criteria(token):

    dim = len(token)//2
    split = token.split(token[dim],1)
    split[0] += token[dim]
    return split



def tokenization(line):

    splices = []
    tokens = line.split()
    for token in tokens:
        split = splitting_criteria(token)
        splices += split
        splices += [' ']

    splices += ['\n']
    return splices


def init_map():
    
    map = {}
    map["\n"] = "1"
    return map


def create_map(document, map):

    count = len(map)
    tokens_map = []
    for line in document:
        tokens = tokenization(line)
        tokens = [el for el in tokens if el != '']
        tokens_map += tokens
        for tok in tokens:
            if tok not in map:
                count +=1
                enc = chr(count)
                while enc in list(map.values()):
                    count +=1
                    enc = chr(count)
                    pass
                map[tok] = chr(count)
    
    return map, tokens_map



def encode_document(string_map, tokens_map, file_path):
     
    replaced = [string_map[token] for token in tokens_map]
    file = open(file_path, 'w', encoding="utf8")
    for el in replaced:
        file.write(el)
    
    file.close()



def decode_document(string_map, file_path):

    document = open_and_check(file_path)
    decoded = []
    keys = list(string_map.keys())
    values = list(string_map.values())
    for row in document:
        for elem in row:
            decoded += keys[values.index(elem)]
    
    
    base = os.path.basename(file_path)
    file = os.path.splitext(base)
    if "encoded_" in file[0]: new_name = file[0].replace("encoded_", "decoded_") + ".txt"
    else: new_name = file[0] + ".txt"
    file = open("./decoded/" + new_name, 'w', encoding="utf8")
    file.write("".join(decoded))
    file.close()
        


def encoding_process(document_path):
    """ """
    
    document = open_and_check(document_path)
    document = document_preprocessing(document)
    map = get_json_file("./res/map.json")
    if len(map) == 0:
        map = init_map()
    map, tokens = create_map(document, map)
    save_json_file("./res/map.json", map)
    base = os.path.basename(document_path)
    file = os.path.splitext(base)
    new_name = "encoded_" + file[0] + ".enc"
    encode_document(map, tokens, './encoded/' + new_name)

    
    
def decoding_process(document_path):
    """ """
    
    map = get_json_file("./res/map.json")
    decode_document(map, document_path)


def print_init_sentence():
    print()
    print("\n***************************************")
    print("Welcome to Simple-Encoding python script")
    print("EXAMPLE USAGE:")
    print("python encoding.py |TYPE|  |FILE|")
    print("WHERE: |TYPE| is one of 'encode' or 'decode' ")
    print("WHERE: |FILE| is the file path (.txt if encode) (.enc if decode)")
    print("Or type each parameter separately!")
    print("***************************************\n")
    
    
def type_content():
    print("Type 1, for encode a document")
    print("Type 2, for decode a document")
    print()
    response = int(input())
    if response == 1:
        print("Enter the document file path to encode. We accept only (.txt) files")
        document_path = str(input())
        encoding_process(document_path)
        
    elif response == 2: 
        print("Enter the document file path to dencode. We accept only (.enc) files")
        document_path = str(input())
        decoding_process(document_path)
    else:
        print("No action")


def check_param():
    """ """
    
    if (sys.argv[1].lower() not in ['encode','decode']):
        print("Error: Bad parameter!")
        print_init_sentence()
        exit()
    
    if (sys.argv[1].lower() == "encode"):
        if (".txt" not in sys.argv[2].lower()):
            print("Error: Bad parameter!")
            print_init_sentence()
            exit()
        else:
            encoding_process(sys.argv[2])
            print("Document " + sys.argv[2] + " encoded succesfully!")
            print("See output in './encoded' \n")
            
            
    if (sys.argv[1].lower() == "decode"):
        if (".enc" not in sys.argv[2].lower()):
            print("Error: Bad parameter!")
            print_init_sentence()
            exit()
        else:
            decoding_process(sys.argv[2])
            print("Document " + sys.argv[2] + " decoded succesfully!")
            print("See output in './decoded' \n")
    
    
def main():
    
    if len(sys.argv) > 1:
        if len(sys.argv) == 3:
            check_param()
        else:
            print("Error: Bad parameter!")
            print_init_sentence()
    else:
        print_init_sentence()
        type_content()
    
    

if __name__ == "__main__":
    main()