from utils import *
import re
import sys
import os

HOME_URL='https://barak8807.editorx.io12/mysite-8'
#HOME_URL='https://fid.dev3'



m = re.search('https?://([A-Za-z_0-9.-]+).*', HOME_URL)
APP_NAME=m.group(1).replace('.', '-')
#APP_NAME=domain_finder(HOME_URL)
 
TEMPLATE_DICT={
    'home_sites_url' : '<<<home.site.url>>>',
}
 
if sys.platform.startswith('win32'):
    NEW_APP_PATH='new-app'    
else:#sys.platform.startswith('linux'):
    NEW_APP_PATH=r'/tmp/new-app'
    os.system('export GOOGLE_APPLICATION_CREDENTIALS=\"WebApps-8cc1b58e690f.json\"')




print('CONFIGURATION:')
print('HOME_URL : ' + HOME_URL)
print('APP_NAME : ' + APP_NAME)
print('TEMPLATE_DICT : ' + str(TEMPLATE_DICT))
print('NEW_APP_PATH : ' + str(NEW_APP_PATH))
