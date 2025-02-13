import csv
import os
import readline
import sys


GREEN = '\x1b[32m'
RESET = '\x1b[0m'


class Completer(object):

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        response = None
        if state == 0:
            if text:
                self.matches = [
                    option
                    for option in self.options
                    if option and option.startswith(text)
                ]
            else:
                self.matches = self.options
        if state < len(self.matches):
            response = self.matches[state]
        else:
            response = None
        return response


if sys.platform == 'darwin':
    readline.parse_and_bind('bind ^I rl_complete')
else:
    readline.parse_and_bind('tab: complete')
readline.set_completer(None)
readline.set_completer_delims('\n')

path = input(GREEN + 'Path to grades csv: ' + RESET).strip()
while not os.path.isfile(path):
    print('File does not exist.')
    print()
    path = input(GREEN + 'Path to grades csv: ' + RESET).strip()
with open(path, mode='r', newline='', encoding='utf-8-sig') as original_csv:
    data = [record for record in csv.DictReader(original_csv)]
    if not data:
        raise Exception('No data.')
original_columns = [column for column in data[0]]
columns = sorted(original_columns)

readline.set_completer(
    Completer(('1', '2')).complete
)
print()
print('Assign grades by\n' +
'1) Name\n' +
'2) UIN'
)
choice = None
while choice not in ('1', '2'):
    choice = input(GREEN + '(type the number without quotes, then press Return): ' + RESET)
if choice == '1':
    key = 'name'
elif choice == '2':
    key = 'uin'
else:
    raise Exception('Impossible state.')

index = dict()
if key == 'name':
    first_columns = [column for column in columns if 'first' in column.lower()]
    last_columns = [column for column in columns if 'last' in column.lower()]
    readline.set_completer(
        Completer([str(i + 1) for i in range(len(first_columns))]).complete
    )
    print()
    print('Which column corresponds to FIRST NAME?')
    for (i, column_name) in enumerate(first_columns, start=1):
        print(f'{i}) {column_name}')
    column_index = None
    while column_index not in list(range(1, len(first_columns) + 1)):
        column_index = int(
            input(
                GREEN +
                '(type the number without quotes, then press Return): ' +
                RESET
            )
        )
    first_name_column = first_columns[column_index - 1]
    readline.set_completer(
        Completer([str(i + 1) for i in range(len(last_columns))]).complete
    )
    print()
    print('Which column corresponds to LAST NAME?')
    for (i, column_name) in enumerate(last_columns, start=1):
        print(f'{i}) {column_name}')
    column_index = None
    while column_index not in list(range(1, len(last_columns) + 1)):
        column_index = int(
            input(
                GREEN +
                '(type the number without quotes, then press Return): ' +
                RESET
            )
        )
    last_name_column = last_columns[column_index - 1]
    for record in data:
        first_name = record[first_name_column]
        last_name = record[last_name_column]
        name = first_name + ' ' + last_name
        if name in index:
            raise Exception('Two students have the same name. Retry with UINs instead. Aborting.')
        index[name] = record
elif key == 'uin':
    uin_columns = [column for column in columns if 'id' in column.lower() or 'uin' in column.lower()]
    readline.set_completer(
        Completer([str(i + 1) for i in range(len(uin_columns))]).complete
    )
    print()
    print('Which column corresponds to UIN?')
    for (i, column_name) in enumerate(uin_columns, start=1):
        print(f'{i}) {column_name}')
    column_index = None
    while column_index not in list(range(1, len(uin_columns) + 1)):
        column_index = int(
            input(
                GREEN +
                '(type the number without quotes, then press Return): ' +
                RESET
            )
        )
    uin_column = uin_columns[column_index - 1]
    for record in data:
        uin = record[uin_column]
        if uin in index:
            raise Exception('Two students have the same UIN. Aborting.')
        index[uin] = record
else:
    raise Exception('Impossible state.')
keys = [key for key in index]

readline.set_completer(
    Completer(columns).complete
)
print()
print(
    GREEN +
    'Type the name of the assessment exactly as it appears on Blackboard (case sensitive).' +
    RESET
)
assessment_column = None
while assessment_column not in columns:
    assessment_column = input('> ')

readline.set_completer(
    Completer(keys).complete
)
print()
print('Begin grading.\nType QUIT at the prompt to stop grading and write file.')
key_prompt = (
    GREEN + 
    (
        'Student: '
        if key == 'name'
        else 'UIN: '
    ) +
    RESET
)
while True:
    print()
    current_key = None
    while current_key != 'QUIT' and current_key not in index:
        current_key = input(key_prompt)
    if current_key == 'QUIT':
        break
    grade = input(GREEN + 'Grade: ' + RESET)
    if grade == 'QUIT':
        break
    index[current_key][assessment_column] = grade

# Should check if this file already exists...
with open('updated_grades.csv', mode='w', newline='') as new_csv:
    csv_writer = csv.DictWriter(new_csv, original_columns)
    csv_writer.writeheader()
    for key in index:
        csv_writer.writerow(index[key])
print()
print('Successfully wrote grades to updated_grades.csv.')
print()
