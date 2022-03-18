from collections import OrderedDict
import requests as r
from filter import read_txt, write_list_to_txt3
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import re, os, xmltodict, json, ast, subprocess, requests, json
import numpy as np
from csv import writer

positions = [0]

asci = ['!','"','#','$','%','&','\',''','(',')','*','+','-','.','/',':',';','<','=',\
'>','?','@','[','\\',']','^','_','`','{','|','}','~']

tokens = {0: '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', 1: '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',
          2: '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', 3: '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'}

tokens_status = {'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': True, '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': True,
                 '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': True, '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': True}

REG_CHANGED = re.compile(".*@@ -(\d+),(\d+) \+(\d+),(\d+) @@.*")

def parse_tree2(tree, keywords, api_sequence):
    if tree is None:
        return None
    for k, v in tree.items():
        if k == '@label' and v in keywords:
            api_sequence.append(v)
            return
        if k == '@type' and v == 'trailer':
            api_sequence.append(v)
        if k == '@type' and v != 'import_from' or v != 'import_name':
            if isinstance(v, OrderedDict):
                parse_tree2(v, keywords, api_sequence)
            if isinstance(v, list):
                for sub_item in v:
                    parse_tree2(sub_item, keywords, api_sequence)

def parse_changes(d, keywords):
    api_sequence = []
    for tree in d:
        parse_tree2(tree, keywords, api_sequence)
    return api_sequence

def filter_dependencies(dep_indicator):
    ml = ['tf','np','pd','tensorflow', 'pytorch', 'numpy', 'pandas', 'keras', 'sklearn']

    deps = []
    x = []
    for item in dep_indicator:
        if item[0] == 'with_stmt' and item[-2] == 'name' and item[-1] != 'name':
            deps.append(item)
        if item[0] == 'with_stmt' and item[1] in ml and item[-1] != 'name' and item[-1] not in asci and '"' not in item[-1] and "'" not in item[-1]:
            deps.append(item)
        if item[0] == 'import_from' or item[0] == 'import_name':
            deps.append(item)

    for keyword in ml:
        for item in deps:
            if keyword in item:
                x.append(item[-1])
    ml = ml + x
    return list(np.unique(ml))
        

def parse_imports(sub_tree, dep_sequence):
    if sub_tree['@type'] != 'suite':
        for k, v in sub_tree.items():
            if v == 'import_from' or v == 'import_name':
                dep_sequence.append(v)
            if k == '@label':
                dep_sequence.append(v)
            if isinstance(v, OrderedDict):
                return parse_imports(v, dep_sequence)
            if isinstance(v, list):
                for sub_item in v:
                    parse_imports(sub_item, dep_sequence)

def parse_with_stmts(sub_tree, with_sequence):
    if sub_tree['@type'] != 'suite':
        for k, v in sub_tree.items():
            if v == 'with_stmt':
                with_sequence.append(v)
            if k == '@label':
                with_sequence.append(v)
            if isinstance(v, OrderedDict):
                return parse_with_stmts(v, with_sequence)
            if isinstance(v, list):
                for sub_item in v:
                    parse_with_stmts(sub_item, with_sequence)

def parse_tree(tree, dep_sequence, with_sequence):
    if tree is None:
        return None
    for k, v in tree.items():
        if k == '@type' and v == 'import_from' or v == 'import_name':
            parse_imports(tree, dep_sequence)
        if k == '@type' and v == 'with_stmt':
            parse_with_stmts(tree, with_sequence)
        if isinstance(v, OrderedDict):
            parse_tree(v, dep_sequence, with_sequence)
        if isinstance(v, list):
            for sub_item in v:
                parse_tree(sub_item, dep_sequence, with_sequence)

def get_ast(pairs):
    p = []
    if not os.path.isdir('./tmp'):
        os.makedirs('./tmp')
    
    with open('./tmp/buggy.py', 'w') as f:
        for line in pairs[0]:
            f.write('{}\n'.format(line))

    with open('./tmp/clean.py', 'w') as f:
        for line in pairs[1]:
            f.write('{}\n'.format(line))
    
    if bool(pairs[0]):
        subprocess.call('pythonparser '+'/media/nimashiri/DATA/vsprojects/tests/tmp/buggy.py >> '+'/media/nimashiri/DATA/vsprojects/tests/tmp/buggy_ast.xml', shell=True)   
        with open("./tmp/buggy_ast.xml") as xml_file:
            buggy_dict = xmltodict.parse(xml_file.read())
        p.append(buggy_dict)

    if bool(pairs[1]):
        subprocess.call('pythonparser '+'/media/nimashiri/DATA/vsprojects/tests/tmp/clean.py >> '+'/media/nimashiri/DATA/vsprojects/tests/tmp/clean_ast.xml', shell=True)
        with open("./tmp/clean_ast.xml") as xml_file:
            clean_dict = xmltodict.parse(xml_file.read())
        p.append(clean_dict)

    return p

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

class WithCollector(ast.NodeVisitor):
    def __init__(self):
        self.withh = {"with": []}
    
    def visit_With(self, node):
        for alias in node.items:
            try:
                if bool(node.items[0].context_expr.func.value.id) and bool(alias.optional_vars):
                    self.withh['with'].append(alias.optional_vars.id)
            except Exception as e:
                continue
        self.generic_visit(node)

    def report(self):
            return self

def tokenize_and_check(pair, api_calls, dependencies, extra_):
    tp = False
    apis = read_txt('./api_list/all.txt')
    a = ' '.join(apis)
    for p in pair:
        for line in p:
            if 'import' not in line or 'from' not in line:
                deps = [dependencies.imports, dependencies.fromm]
                for item in deps:
                    for key, value in item.items():
                        for f in value:
                            for v in f:
                                if v is not None:
                                    if 'torch.' in v or 'tf.' in v\
                                        or 'np.' in v in v or 'pd.' in v or 'keras' in v \
                                            or 'sklearn' in v or 'torchvision' in v or 'torchvision.' in v:
                                            k = [item for item in extra_.withh['with'] if item in line]
                                            if v in line or bool(k):
                                                tp = True
                                                break
    return tp

def get_changes_decompose_patches(_patches):
    out = {}
    buggy = []
    clean = []
    string_check= re.compile('[@]') 
    for i, p in enumerate(_patches):
        temp = p.copy()
        for line in temp:
            if line[0] == '+':
                temp.remove(line)
            if re.findall(r'^(\s*""").*$', line):
                temp.remove(line)
                
        temp2 = p.copy()
        for line in temp2:
            if line[0] == '-':
                temp2.remove(line)
            if re.findall(r'^(\s*""").*$', line):
                temp2.remove(line)

        for idx, line in enumerate(temp):
            if line[0] == '-':
                line =  line[:0] + line[0+1:]
                temp[idx] = line
            if string_check.search(line):
                temp.remove(line)

        for idx, line in enumerate(temp2):
            if line[0] == '+':
                line =  line[:0] + line[0+1:]
                temp2[idx] = line
            if string_check.search(line):
                temp2.remove(line)
                
        out[i] = [temp, temp2]
    return out

def get_added_deleted_lines(_patches):
    changes = {}
    change_statistics = {}
    for i, p in enumerate(_patches):
        buggy_ = []
        clean_ = []
        j = 0
        k = 0
        for line in p:
            if len(line) > 1:
                if line[0] == '-':
                    j += 1
                    line =  line[:0] + line[0+1:]
                    buggy_.append(line)
                if line[0] == '+':
                    k += 1
                    line =  line[:0] + line[0+1:]
                    clean_.append(line)
            changes[i] = [buggy_, clean_]
            change_statistics[i] = [j, k, j + k]
    return changes, change_statistics


def select_access_token(current_token):
    x = ''
    if all(value == False for value in tokens_status.values()):
        for k, v in tokens_status.items():
            tokens_status[k] = True

    for k, v in tokens.items():
        if tokens_status[v] != False:
            x = v
            break
    current_token = x
    return current_token

def get_changes_line_level(_patches):
    changes = {}
    for i, p in enumerate(_patches):
        buggy_ = []
        clean_ = []
        for line in p:
            c = False
            if line[0] == '-':
                line =  line[:0] + line[0+1:]
                buggy_.append(line)
            if line[0] == '+':
                line =  line[:0] + line[0+1:]
                clean_.append(line)
                c = True
            if c:
                changes[i] = [buggy_, clean_]
                buggy_ = []
                clean_ = [] 
    return changes

def get_patches(splitted_lines):
    super_temp = []
    j = 0
    indices = []
    while j < len(splitted_lines):
        if splitted_lines[j][0] == '@':
            indices.append(j)
        j += 1

    if len(indices) == 1:
        for i, item in enumerate(splitted_lines):
            if i != 0:
                super_temp.append(item)
        super_temp = [super_temp]
    else:
        i = 0
        j = 1
        while True:
            temp = [] 
            for row in range(indices[i]+1, indices[j]):
                temp.append(splitted_lines[row])
            super_temp.append(temp)
            if j == len(indices)-1:
                temp = [] 
                for row in range(indices[j]+1, len(splitted_lines)):
                    temp.append(splitted_lines[row])
                super_temp.append(temp)
                break
            i+= 1
            j+= 1
    return super_temp

def parse_dependencies(new_sequence):
    j = 0
    indices = []
    super_temp = []
    while j < len(new_sequence):
        if new_sequence[j] == 'import_from' or new_sequence[j] == 'import_name' or new_sequence[j] == 'with_stmt':
            indices.append(j)
        j += 1

    i = 0
    j = 1
    while True:
        temp = []
        for row in range(indices[i], indices[j]):
            temp.append(new_sequence[row])
        super_temp.append(temp)
        if j == len(indices)-1:
            temp = [] 
            for row in range(indices[j], len(new_sequence)):
                temp.append(new_sequence[row])
            super_temp.append(temp)
            break
        i += 1
        j += 1
    return super_temp

import random, os

def main():
    current_dir = os.getcwd()
    row_counter = 0
    current_token = tokens[0]
    for root, dir, libs in os.walk('/media/nimashiri/DATA/vsprojects/Machine Learning API Bug Detection/commits'):
        for lib in libs:
            current_file = os.path.join(root, lib)
            data = read_txt(current_file)
            #data = random.sample(data, len(data))
            #api_fixed_text = 'https://api.github.com/repos/'
            for counter, llink in enumerate(data):
                    l = llink.split('/')
                    v = "https://github.com/{0}/{1}{2}".format(l[3],l[4],'.git')
                    subprocess.call('git clone '+v+' '+current_dir+'/cloned_project', shell=True)
                    
                    #l = llink.split('/')

                    #llink = api_fixed_text+l[3]+'/'+l[4]+'/commits'+'/'+l[-1]

                    #response = requests_retry_session().get(llink, headers={'Authorization': 'token {}'.format(current_token)})


                    # if response.status_code != 200:
                    #     tokens_status[current_token] = False
                    #     current_token = select_access_token(current_token)
                    #     response = requests_retry_session().get(llink, headers={
                    #         'Authorization': 'token {}'.format(current_token)})

                    # if response.status_code != 200:
                    #     tokens_status[current_token] = False
                    #     current_token = select_access_token(current_token)
                    #     response = requests_retry_session().get(llink, headers={
                    #         'Authorization': 'token {}'.format(current_token)})

                    # if response.status_code != 200:
                    #     tokens_status[current_token] = False
                    #     current_token = select_access_token(current_token)
                    #     response = requests_retry_session().get(llink, headers={
                    #         'Authorization': 'token {}'.format(current_token)})

                    # if response.status_code != 200:
                    #     tokens_status[current_token] = False
                    #     current_token = select_access_token(current_token)
                    #     response = requests_retry_session().get(llink, headers={
                    #         'Authorization': 'token {}'.format(current_token)})


                    # print('The connection is ok {}'.format(response.status_code))
                    # x = json.loads(response.text)
                    files = x['files']
                    for i, file in enumerate(files):
                        if file['filename'].endswith('.py'):
                            try:
                                raw_code = r.get(file['raw_url'])
                                write_list_to_txt3(raw_code.text, './code.py')
                                
                                _patch = file['patch']
                                splitted = _patch.split('\n')

                                _patches = get_patches(splitted)

                                out_only_changes, change_statistics = get_added_deleted_lines(_patches)

                                out_full_patch = get_changes_decompose_patches(_patches)

                                if not os.path.isdir('./tmp'):
                                    os.makedirs('./tmp')

                                #subprocess.call('pythonparser '+'/media/nimashiri/DATA/vsprojects/tests/code.py >> '+'/media/nimashiri/DATA/vsprojects/tests/code.xml', shell=True)
                                subprocess.call('pythonparser '+'/media/nimashiri/DATA/vsprojects/tests/code.py >> '+'/media/nimashiri/DATA/vsprojects/tests/code.xml', shell=True)

                                with open("code.xml", "r", encoding='utf8') as xml_file:
                                    code = xmltodict.parse(xml_file.read())
                                dep_sequence = []
                                with_sequence = []

                                parse_tree(code, dep_sequence, with_sequence)
                                new_seq = dep_sequence + with_sequence
                                dep_indicator = parse_dependencies(new_seq)

                                for _change in out_only_changes:
                                    d = get_ast(out_only_changes[_change])
                                    keywords = filter_dependencies(dep_indicator)
                                    api_sequence = parse_changes(d, keywords)

                                    if bool(api_sequence):
                                        for item in keywords:
                                            if any(item in s for s in api_sequence):
                                                print('API existing for {}'.format(item))
                                                if api_sequence.index(item) < api_sequence.index('trailer'):
                                                    if change_statistics[_change][2] <= 4:
                                                        if bool(change_statistics[_change][2]):
                                                            with open('./dataset/data4.csv', 'a', newline='\n') as fd:
                                                                field_names = ['No', 'Library name', 'Commit link', 'File name', 'Raw url',\
                                                                    'Buggy Path', 'Clean Path', 'Buggy Changes', 'Clean Changes',\
                                                                    '# Actual deleted lines', '# Actual added lines', '# Deleted lines', '# Added lines',
                                                                    'Keywords', 'Dependencies']
                                                                    
                                                                writer_object = writer(fd)

                                                                a  = '\\n'.join(out_full_patch[_change][0])
                                                                b = '\\n'.join(out_full_patch[_change][1])
                                                                c = '\\n'.join(out_only_changes[_change][0])
                                                                d = '\\n'.join(out_only_changes[_change][1])
                                                                my_data = [row_counter, lib, llink, file['filename'], file['raw_url'], a, b, \
                                                                c, d, file['deletions'], file['additions'], change_statistics[_change][0],\
                                                                    change_statistics[_change][1]]
                                                            
                                                            writer_object.writerow(my_data)
                                                    if change_statistics[_change][2] > 4 and change_statistics[_change][2] <=15:
                                                            if bool(change_statistics[2]):
                                                                with open('./dataset/data15.csv', 'a', newline='\n') as fd:     
                                                                    writer_object = writer(fd)

                                                                    a  = '\\n'.join(out_full_patch[_change][0])
                                                                    b = '\\n'.join(out_full_patch[_change][1])
                                                                    c = '\\n'.join(out_only_changes[_change][0])
                                                                    d = '\\n'.join(out_only_changes[_change][1])
                                                                    my_data = [row_counter, lib, llink, file['filename'], file['raw_url'], a, b, \
                                                                    c, d, file['deletions'], file['additions'], change_statistics[_change][0],\
                                                                                    change_statistics[_change][1]]
                                                                                
                                                                    writer_object.writerow(my_data)
                                                    else:
                                                        if bool(change_statistics[_change][2]):
                                                            with open('./dataset/data20.csv', 'a', newline='\n') as fd:
                                                                writer_object = writer(fd)

                                                                a  = '\\n'.join(out_full_patch[_change][0])
                                                                b = '\\n'.join(out_full_patch[_change][1])
                                                                c = '\\n'.join(out_only_changes[_change][0])
                                                                d = '\\n'.join(out_only_changes[_change][1])
                                                                my_data = [row_counter, lib, llink, file['filename'], file['raw_url'], a, b, \
                                                                c, d, file['deletions'], file['additions'], change_statistics[_change][0],change_statistics[_change][1]]
                                                                                
                                                                writer_object.writerow(my_data)

                                                    row_counter += 1
                                                    #write_list_to_txt2(out_full_patch[_change][0], './dataset/buggy'+str(counter)+'.py')
                                                    #write_list_to_txt2(out_full_patch[_change][1], './dataset/clean'+str(counter)+'.py')

                                    subprocess.call('rm -rf tmp', shell=True)
                                    
                            except Exception as e:
                                print(e)
                                subprocess.call('rm -rf tmp', shell=True)

                        subprocess.call('rm -rf code.xml', shell=True)


if __name__ == '__main__':
    main()