import os
import re
import json

script_path = os.path.split(os.path.realpath(__file__))[0]
settings_file_path = script_path + '/TJSSE/settings.py'
profile_path = script_path + '/setup.json'
bash_file_path = script_path + '/sub_setup.sh'

profile_fin = open(profile_path, 'r')
profile_json = json.loads(profile_fin.read())
fin = open(settings_file_path, 'r')
settings_str = fin.read()

link = re.compile(r'DATABASES\s*=\s*\{.*\}', re.M | re.S)

instead_database = "DATABASES = { 'default': { "
for ele in profile_json['DATABASES']:
    instead_database += "'%s': '%s', " % (ele, profile_json['DATABASES'][ele])
instead_database += "} }"

settings_str = re.sub(link, instead_database, settings_str)
with open(settings_file_path, 'w') as fout:
    fout.write(settings_str)

os.system(bash_file_path + ' ' + profile_json['django'])
