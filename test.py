code = '0011111110110101'
# '0011 00001 11001 00'
# 0001 00001 00010 00
# 0101 0000 10010101
num = int(code, 2)


# first = num & 0b11
# print(bin(first))

# kedua = (num >> 2) & 0b11111
# print(bin(kedua))

# ketiga = (num >> 7) & 0b11111
# print(bin(ketiga))

keempat = (num >> 12) & 0b1111 == 0b0011
print(bin((num >> 12) & 0b1111), keempat)