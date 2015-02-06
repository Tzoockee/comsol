connString = 'DB_Connection'
documentsIdSeed = 'Start_Seed'
settings = {}

if len(settings) == 0:
    with open('admin.cfg') as f:
        content = f.readlines()

    for line in content:
        if len(line) > 0 and line[0] != '#':
            values = line.split(' = ')
            if len(values) == 2:
                settings[values[0]] = values[1].rstrip()


