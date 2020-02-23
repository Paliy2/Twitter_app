import json
import os
import pprint


def parse_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
    # type dict

    # type list
    # if len list == 1: enter list


def print_list(lst):
    for item in lst:
        print(str(item + '; '), end='')
    print()


def info():
    result = "To restart , just type 'R'\n"
    result += "Enter names properly. You can view data bu pressin 'data'\n"
    result += "To quit press 'q'\n"
    result += 'You can view help anytyme you press "help"\n'
    return result


def check_input(keyboard, data, file_name):
    keyboard = keyboard.lower()
    if keyboard == 'q':
        print('Bye-bye')
        return 'exit'

    if keyboard == 'r':
        data = parse_json(file_name)

    if keyboard == 'help':
        print()
        print(info())

    if keyboard == 'data':
        pprint.pprint(data)
        print(data)

    return data


def main():
    print(info())
    file_name = input('Enter a json file to observe: ')
    files = os.listdir()
    if file_name not in files:
        print('No such file in directory.')
        file_name = 'kved.json'
    data = parse_json(file_name)

    keyboard = 'keyboard input data'
    while True:
        exit = check_input(keyboard, data, file_name)
        if exit == 'exit':
            return
        elif type(exit) is not str:
            data = exit

        if type(data) is dict:
            print('You can choose from: ')
            possible_keys = list(data.keys())
            print_list(possible_keys)
            keyboard = input('Enter object from file: ')
            check_input(keyboard, data, file_name)
            if keyboard in possible_keys:
                data = data[keyboard]
            else:
                continue

        elif type(data) is list:
            print('The data type is list.')
            view = input('Do you want to view it?(Yes or No): ')
            check_input(view, data, file_name)

            if view.lower() == 'yes' or view.lower() == 'y':
                print(data)

            print('The total amount of items in list is ', len(data))
            number = input('Enter number you want to view: ')
            check_input(number, data, file_name)
            try:
                number = int(number)
                if abs(number) >= len(data):
                    int('raise error')
            except:
                print('Error: wrong number. \nRestarting...')
                continue
            if abs(number) < len(data):
                data = data[number - 1]
                print(data)

        if type(data) is str:
            print('Value founded: ', data)
            input('press any key to start again: ')
            keyboard = 'r'

        elif type(data) is list and len(data) == 1:
            data = data[0]


if __name__ == '__main__':
    main()
