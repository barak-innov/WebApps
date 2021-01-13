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
    request_json = request.get_json(silent=True)
    request_args = request.args
    # clean old runs history
    print('clean old runs history')
    shutil.rmtree('new-app', ignore_errors=True)

    # ------------------------------------------------

    # Createing the github project
    headers = {'PRIVATE-TOKEN': 'cCmRuMVWg-K8SkpcQrS5'}
    resp = requests.post('https://gitlab.com/api/v4/projects?name=' + APP_NAME + '&namespace_id=10638272', headers=headers, allow_redirects=True)
    ## TODO: add checking of the response

    # ------------------------------------------------

    # Add the project to repository
    ## create all files of new app
    copytree('template-app', 'new-app')

    ## apply the pach on the files in the new-app. the pathc allow to replace strings in the app
    forceCopyFile('app_patch_templates/constants.dart.template', 'new-app/lib/constants.dart')

    ## apply new app configuration(like the domain) on the new-app project
    inplace_change('new-app/lib/constants.dart', TEMPLATE_DICT['home_sites_url'], HOME_URL)

    # ------------------------------------------------

    # Upload project to the new git repository
        
    subprocess.Popen(['git','config','--global','user.name', GIT_USERNAME], cwd=r'new-app').wait()
    subprocess.Popen(['git','config','--global','user.password', GIT_PASSWORD], cwd=r'new-app').wait()

    subprocess.Popen(['git','init'], cwd=r'new-app').wait()
    subprocess.Popen(['git', 'remote', 'add', 'origin', 'https://gitlab.com/web-apps-group-auto-updated/' + APP_NAME + '.git'], cwd=r'new-app').wait()
    subprocess.Popen(['git', 'add', '.'], cwd=r'new-app').wait()
    subprocess.Popen(['git','commit','-m','"Initial commit"'], cwd=r'new-app').wait()
    subprocess.Popen(['git','push','-u','origin','master'], cwd=r'new-app').wait()


    # ------------------------------------------------

    # Start the build with codemagic
