class HexDump:
    def __init__(self, block_address):
        self.block_address = block_address

    def dumpv2(self, start, end):
        if end > len(self.block_address):
            raise "Out of memory"
        print("\n ADDRESS     -->  ", end="")
        for i in range(0, 16):
            print(format(i, "X").zfill(2), end=" ")
        print("\n")

        ybytes = []
        xbytes = []
        for y in range(start, end):
            value_bin = format(self.block_address[y], "X")
            for cut in range(0, len(value_bin), 2):
                xbytes.append(value_bin[cut : cut + 2])
                if len(xbytes) >= 16:
                    ybytes.append(xbytes)
                    xbytes = []

        zero = False
        printed = False
        for idx, y in enumerate(ybytes):
            addrs = format(idx * 16, "X").zfill(8)

            if not zero:
                print(f" 0x{addrs}  -->  ", end="")
                for x in y:
                    print(f"{str(x).zfill(2)}", end=" ")
                print("  -->  ", end="")
                for x in y:
                    try:
                        decode_hex1 = bytes.fromhex(x).decode(
                            "windows-1252", errors="replace"
                        )
                        if not decode_hex1.isprintable():
                            print(".", end=" ")
                        else:
                            print(decode_hex1, end=" ")

                    except IndexError:
                        print("    ", end="")
                    except:
                        print(".", end=" ")

                print("")
            else:
                if not printed:
                    print(' *')
                    printed = True

            if "".join(y) == "0000000000000000":
                zero = True
            else:
                if printed:
                    print(addrs)
                    
                zero = False
                printed = False
