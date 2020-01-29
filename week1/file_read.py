import os.path

while True:
    filename = input('Filename:')
    if not os.path.isfile(filename):
        print('File:', filename, ' is not exists')
        continue
    file = open(filename, 'r')
    while True:
        line = file.readline()
        if not line:
            print('No lines left')
            break
        print(line)
        user_command = input()
        if user_command == 'n':
            break
