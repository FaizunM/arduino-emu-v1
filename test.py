b = 0b11101010
c = 0b10010010

x = (b << 8) | c
z = x >> 8
print(format(z, 'b').zfill(8))