import requests
from config import *
from time import sleep
import subprocess
from login_config import *
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
    return 'Hello f!'
"""





def main_http(request):
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


if __name__ == '__main__':
    main_http({});