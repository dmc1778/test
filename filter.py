import os
import numpy as np

def write_list_to_txt3(data, filename):
    with open(filename, "w", encoding='utf-8') as file:
        file.write(data+'\n')

def write_list_to_txt2(data, filename):
    with open(filename, "w") as file:
        for row in data:
            file.write(row+'\n')

def read_txt(fname):
    with open(fname, 'r') as fileReader:
        data = fileReader.read().splitlines()
    return data
        
def main():
    for root, dir, files in os.walk('./repos_phase1'):
        for file in files:
            current_file = os.path.join(root, file)
            data = read_txt(current_file) 
            data = np.unique(data)
            filename = os.path.join('D:\\vsprojects\\Machine Learning API Bug Detection\\repos_phase2', file)
            write_list_to_txt2(data, filename)



if __name__ == '__main__':
    main()











