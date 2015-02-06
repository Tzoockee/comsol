import glob

config_file = ''
if config_file == '':
    for file in glob.glob('*.cfg')[:1]:
        config_file = file

connString = 'DB_Connection'
documentsIdSeed = 'Start_Seed'
settings = {}

if len(settings) == 0:
    with open(config_file) as f:
        content = f.readlines()

    for line in content:
        if len(line) > 0 and line[0] != '#':
            values = line.split(' = ')
            if len(values) == 2:
                settings[values[0]] = values[1].rstrip()

