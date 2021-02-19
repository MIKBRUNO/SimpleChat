from io import BytesIO

msg = b'HelloWorld'
io = BytesIO(msg)
# io.write(msg)
print(io.read())
