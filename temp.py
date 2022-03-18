import pandas as pd
from csv import reader
import random, csv

def write_list_to_txt2(data, filename):
    with open(filename, "w") as file:
        for row in data:
            file.write(row+'\n')

def write_list_to_txt3(data, filename):
    with open(filename, "w", encoding='utf-8') as file:
        file.write('\n'.join(data))

def myfunction():
  return 0.1

def main():
    data = []
    
    with open('./dataset/data.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)

    # for i in range(1, len(list_of_rows)):
    #     if (int(list_of_rows[i][11]) + int(list_of_rows[i][12]) < 20):
    #         data.append(list_of_rows[i])
            
    list_of_rows = random.sample(list_of_rows, len(list_of_rows))
    x_random = random.choices(list_of_rows, k=370)

    # with open('./code_samples/sample_data.csv','w') as result_file:
    #     wr = csv.writer(result_file, dialect='excel')
    #     wr.writerows(x_random)

    comms = []
    for i, row in enumerate(x_random):
        if int(row[11])+int(row[12]) < 20:
            if bool(row[7]) and bool(row[8]):
                comms.append(row[2])
                x1 = row[7].split('\\n')
                x2 = row[8].split('\\n')
                write_list_to_txt3(x1, './code_samples2/'+str(i)+'_sample_'+str(1)+'.py')
                write_list_to_txt3(x2, './code_samples2/'+str(i)+'_sample_'+str(2)+'.py')

    write_list_to_txt2(comms, './code_samples2/commits.txt')

if __name__ == '__main__':
    main()