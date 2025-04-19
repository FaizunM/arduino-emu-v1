class HexDump:
    def __init__(self, block_address):
        self.block_address = block_address

    def dump(self, start, end):
        if end > len(self.block_address):
            raise "Out of memory"
        print("\n ADDRESS     -->  ", end="")
        for i in range(0, 16):
            print(format(i, "X").zfill(2), end=" ")
        print("\n")
        for y in range(start, end - 1, 8):
            addrs = format(y, "X").zfill(8)

            print(f" 0x{addrs}  -->  ", end="")
            for x in range(y, y + 8):
                try:
                    hexval = format(self.block_address[x], "X").zfill(4)
                    print(hexval[2:], end=" ")
                    print(hexval[:2], end=" ")
                except:
                    print("      ", end="")

            print(f"  -->   ", end="")
            for x in range(y, y + 8):
                try:
                    hexval = format(self.block_address[x], "X").zfill(4)
                    decode_hex1 = bytes.fromhex(hexval[2:]).decode("windows-1252", errors='replace')
                    if not decode_hex1.isprintable():
                        print('.', end=' ')
                    else:
                        print(decode_hex1, end=" ")
                    
                    decode_hex2 = bytes.fromhex(hexval[:2]).decode("windows-1252", errors='replace')
                    if not decode_hex2.isprintable():
                        print('.', end=' ')
                    else:
                        print(decode_hex2, end=" ")
                except IndexError:
                    print("    ", end="")
                except:
                    print(".", end=" ")

            print("")
