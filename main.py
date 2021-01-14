import requests
from time import sleep
import subprocess
from login_config import *
from google.cloud import logging
import json
from types import SimpleNamespace
from utils import *
import re
import sys
import os

"""
def my_func_http(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return 'App Pushed Successfuly'
"""




def main_http(request):
    ####
    #######
    ##########
    ####
    #######
    ##########
    # CONFIG
    ####
    #######
    ##########
    ####
    #######
    ##########
    request_args = request.args
    HOME_URL = request_args['web_url']
    m = re.search('https?://([A-Za-z_0-9.-]+).*', HOME_URL)
    APP_NAME=m.group(1).replace('.', '-')
    
    TEMPLATE_DICT={
        'home_sites_url' : '<<<home.site.url>>>',
    }
    
    if sys.platform.startswith('win32'):
        NEW_APP_PATH='new-app'    
        os.system('set GOOGLE_APPLICATION_CREDENTIALS=\"WebApps-8cc1b58e690f.json\"')
    else:#sys.platform.startswith('linux'):
        NEW_APP_PATH=r'/tmp/new-app'
        os.system('export GOOGLE_APPLICATION_CREDENTIALS=\"WebApps-8cc1b58e690f.json\"')




    print('CONFIGURATION:')
    print('HOME_URL : ' + HOME_URL)
    print('APP_NAME : ' + APP_NAME)
    print('TEMPLATE_DICT : ' + str(TEMPLATE_DICT))
    print('NEW_APP_PATH : ' + str(NEW_APP_PATH))

    done_msg='{"msg":"App Runs Successfuly", "args":"'+str(request_args)+'"}'
    faile_msg='App Build&Deploy Failed'
    headers={}


    ####
    #######
    ##########
    ####
    #######
    ##########
    # RUN THE LOGIC
    ####
    #######
    ##########
    ####
    #######
    ##########
    try:
        
        # request_json = request.get_json(silent=True)
        # request_args = request.args
        # clean old runs history
        print('clean old runs history')
        shutil.rmtree(NEW_APP_PATH, ignore_errors=True)

        # ------------------------------------------------

        # Createing the github project
        headers = {'PRIVATE-TOKEN': 'cCmRuMVWg-K8SkpcQrS5'}
        resp = requests.post('https://gitlab.com/api/v4/projects?name=' + APP_NAME + '&namespace_id=10638272', headers=headers, allow_redirects=True)
        ## TODO: add checking of the response

        # ------------------------------------------------

        # Add the project to repository
        ## create all files of new app
        print('creating new app...')
        copytree('template-app', NEW_APP_PATH)
        print('creating new app...DONE!')

        ## apply the pach on the files in the new-app. the pathc allow to replace strings in the app
        print('appling patch on files...')
        forceCopyFile('app_patch_templates/constants.dart.template', NEW_APP_PATH + '/lib/constants.dart')
        print('appling patch on files...DONE!')

        ## apply new app configuration(like the domain) on the new-app project
        print('replace strings in pached files...')
        inplace_change(NEW_APP_PATH + '/lib/constants.dart', TEMPLATE_DICT['home_sites_url'], HOME_URL)
        print('replace strings in pached files...DONE!')

        # ------------------------------------------------

        # Upload project to the new git repository
        subprocess.Popen(['git','config','--global','user.name', GIT_USERNAME], cwd=NEW_APP_PATH).wait()
        subprocess.Popen(['git','config','--global','user.password', GIT_PASSWORD], cwd=NEW_APP_PATH).wait()
        subprocess.Popen(['git','config','--global','user.email', GIT_EMAIL], cwd=NEW_APP_PATH).wait()
        subprocess.Popen(['git','init'], cwd=NEW_APP_PATH).wait()
        subprocess.Popen(['git', 'remote', 'add', 'origin', 'https://' + GIT_TOKEN_NAME + ':' + GIT_TOKEN_VALUE + '@gitlab.com/web-apps-group-auto-updated/' + APP_NAME + '.git'], cwd=NEW_APP_PATH).wait()
        subprocess.Popen(['git', 'add', '.'], cwd=NEW_APP_PATH).wait()
        subprocess.Popen(['git','commit','-m','"Initial commit"'], cwd=NEW_APP_PATH).wait()
        subprocess.Popen(['git','push','-u','origin','master', '--force'], cwd=NEW_APP_PATH).wait()
        # ------------------------------------------------

        # Start the build with codemagic

        
        print(done_msg)
        return (done_msg, 403, headers)
    except Exception as err:
        return (faile_msg + ', due to: ' + str(err), 404, headers)


# if __name__ == '__main__':
#     request_fake_params = "{\"args\": {\"web_url\": \""+HOME_URL+"\"}}"
#     request_fake_obj = json.loads(request_fake_params, object_hook=lambda d: SimpleNamespace(**d))
#     main_http(request_fake_obj);