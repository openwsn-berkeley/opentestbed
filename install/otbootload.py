import subprocess
import shutil
import json
import requests
import time

firmware_load = 'otswtoload.json'
code_folder   = 'latest'
output_file   = 'latest.zip'
download_success   = 1

# wait until internet access ok
while True:
    try:
        requests.get('https://www.google.com')
        break
    except:
        pass
    time.sleep(1)

file_to_download   = {}

try:
    # get file
    shutil.copyfile('{0}/{1}'.format(code_folder,firmware_load), firmware_load)
    # open json file
    with open(firmware_load, 'r') as f:
        file_to_download    = f.read()
    # get dictionary
    file_to_download = json.loads(file_to_download)
    # try 10 times to download the file
    for i in range(1,10):
        download_success  = subprocess.call(['wget', '-O', output_file, file_to_download['url'] ])
        if download_success==0:
            subprocess.call(['unzip', '-o', output_file])
            subprocess.call(['rm', '-r', code_folder])
            subprocess.call('mv opentestbed* latest', shell=True)
            break
        else:
            time.sleep(1)

    if download_success==0:
        file_to_download['last_changesoftware_succesful']  = True
    else:
        file_to_download['last_changesoftware_succesful']  = False
except:
        file_to_download['last_changesoftware_succesful']  = False

with open('{0}/{1}'.format(code_folder,firmware_load), 'w') as f:
    f.write(json.dumps(file_to_download))

subprocess.call(['supervisorctl', 'start', 'otbox'])
