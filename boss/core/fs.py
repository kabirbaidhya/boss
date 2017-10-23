'''
Boss core file system utilities.
'''


def read(filename):
    ''' Read contents of file and return it. '''
    with open(filename, 'r') as f:
        return f.read()


def write(filename, data):
    ''' Write data to the file. '''
    with open(filename, 'w') as f:
        f.write(data)
