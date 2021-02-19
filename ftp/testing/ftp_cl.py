import ftplib as ftp
import os

ftp_cl = ftp.FTP()
ftp_cl.connect('localhost', 9091)
print(ftp_cl.login('mik', '3216547'))
with open('hello.txt', 'rb') as fil:
    ftp_cl.storlines('STOR hello_ftp.txt', fil)
with open('hello_from_ftp.txt', 'w') as f:
    f.write(ftp_cl.retrlines('RETR hello_ftp.txt', f.write))
while True:
    pass
