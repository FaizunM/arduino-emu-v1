code = 0b11111111000000001001000000100000

k = (code >> 16) & 0xFFFF

d = (code >> 4 ) & 0b11111


print(k, d)