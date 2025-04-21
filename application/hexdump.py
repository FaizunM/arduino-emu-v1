class HexDump:
    def __init__(self, array_block):
        self.ybytes = []
        self.y_decoded = []
        self.array_block = array_block
        
    def generate(self, start, stop):
        xbytes = []
        x_decoded = []

        for y in range(
            start,
            stop,
        ):
            value_bin = format(self.array_block[y], "X").zfill(8)
            for cut in range(0, len(value_bin), 2):
                xbytes.append(value_bin[cut : cut + 2])
                try:
                    decode_hex1 = bytes.fromhex(value_bin[cut : cut + 2]).decode(
                        "windows-1252", errors="replace"
                    )
                    if not decode_hex1.isprintable():
                        x_decoded.append(".")
                    else:
                        x_decoded.append(decode_hex1)
                except:
                    x_decoded.append(".")
                if len(xbytes) >= 16:
                    self.ybytes.append(xbytes)
                    self.y_decoded.append(x_decoded)

                    xbytes = []
                    x_decoded = []

    def dump(self, render_root, address_pointer, height):
        render_root.addstr(1, 2, f"ADDRESS")
        render_root.addstr(1, 67, "DECODE (Windows-1252)")
        for i in range(0, 16):
            render_root.addstr(1, (i * 3) + 17, f"{format(i, 'X').zfill(2)}")
        self.ybytes = []
        self.y_decoded = []
        for num_line in range(0 + 3, height):
            self.generate(
                0 + (num_line - 3) + (address_pointer * 4),
                32 + (num_line - 3) + (address_pointer * 4),
            )
            render_root.addstr(
                num_line,
                2,
                f"{format(((address_pointer) + (num_line - 3) * 16), 'X').zfill(8)}",
            )
            render_root.addstr(num_line, 12, "-->")
            render_root.addstr(
                num_line,
                17,
                " ".join(self.ybytes[(num_line - 3)]),
            )
            render_root.addstr(
                num_line,
                67,
                " ".join(self.y_decoded[(num_line - 3)]),
            )
