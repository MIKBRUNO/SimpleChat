import ftplib as ftp

ftp_cl = ftp.FTP()
ftp_cl.connect('localhost', 9091)
print(ftp_cl.login('mik', '3216547'))
while True:
    pass
