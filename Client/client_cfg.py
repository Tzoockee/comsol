docRepositoryPath = ''
DB_Connection = ''

if docRepositoryPath == '' and DB_Connection == '':
    with open('client.cfg') as f:
        content = f.readlines()

    for line in content:
        if len(line) > 0 and line[0] != '#':
            values = line.split(' = ')
            if len(values) == 2:
                if values[0] == 'docRepositoryPath':
                    docRepositoryPath = values[1].rstrip()
                if values[0] == 'DB_Connection':
                    DB_Connection = values[1].rstrip()

