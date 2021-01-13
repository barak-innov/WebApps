from utils import *
import re
HOME_URL='https://barak8807.editorx.io8/mysite-8'
#HOME_URL='https://fid.dev3'



m = re.search('https?://([A-Za-z_0-9.-]+).*', HOME_URL)
APP_NAME=m.group(1).replace('.', '-')
#APP_NAME=domain_finder(HOME_URL)
 
TEMPLATE_DICT={
    'home_sites_url' : '<<<home.site.url>>>',
}


print('CONFIGURATION:')
print('HOME_URL : ' + HOME_URL)
print('APP_NAME : ' + APP_NAME)
print('TEMPLATE_DICT : ' + str(TEMPLATE_DICT))
