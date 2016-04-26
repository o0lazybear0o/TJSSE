import os
import re

script_path = os.path.split(os.path.realpath(__file__))[0]
file_path = script_path + '/TJSSE/settings.py'
fin = open(file_path, 'r')
settings_str = fin.read()
link = re.compile(r'DATABASES\s*=\s*\{.*\}', re.M | re.S)
settings_str = re.sub(link,
                      """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': 'sseadmin.',
        'HOST': '10.60.45.70',
        'PORT': '3306',
    }
}""", settings_str)
with open(file_path, 'w') as fout:
    fout.write(settings_str)
	
bash_file_path = script_path + '/sub_setup.sh'
os.system(bash_file_path)