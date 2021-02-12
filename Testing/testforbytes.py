m = b'1'
i = int.from_bytes(m, 'little')
# i = pow(i, 12012, 2134)
print(i.to_bytes(i.bit_length()//8 + 1, 'big'))

