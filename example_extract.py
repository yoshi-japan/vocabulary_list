import pathlib
import csv
import re


def extract_example(input_from_csv):
    re_pattern = '<div class="ex">(<span>[^<]*</span>)?[^/]*/em></div>'
    findall_example_list = re.findall(re_pattern, input_from_csv)
    return findall_example_list


output_path = pathlib.Path.cwd()/ 'done' / 'output'
path = pathlib.Path.cwd() / 'done' / 'new_one'
t = path.glob("*.csv")

original_files = [i for i in t]
# for _ in original_files:
#     print(_.stem)

output_files = ["ex_" + file.name for file in original_files]


def write_files():
    print('hello')
    for original_name,output_name in zip(original_files,output_files):
        write_name = output_path / output_name
        print(write_name, type(write_name))
        with open(original_name, 'r', encoding='utf-8-sig') as reading_file,\
                open(write_name, 'w', encoding='utf-8', newline='') as writing_file:
            csv_reader = csv.reader(reading_file)
            csv_writer = csv.writer(writing_file)

            for line in csv_reader:
                joined_list = ''.join(extract_example(line[1]))
                csv_writer.writerow([line[0], joined_list])

            str_name = str(original_name)
            print('done'+ str_name)


write_files()