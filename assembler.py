from assembler import Assembler
import sys, os, struct

if __name__ == "__main__":
    args = sys.argv[1:]

    lines = []
    for idx, arg in enumerate(args):
        if arg == "-i":
            with open(os.path.abspath(args[idx + 1]), "r") as f:
                for line in f.readlines():
                    line = line.replace("\n", "").replace("    ", "")
                    lines.append(line)
                f.close()

        if arg == "-o":
            assembler = Assembler(lines)
            compiled = assembler.compile()

            data = struct.pack("<" + "I" * len(compiled), *compiled)
            with open(os.path.abspath(args[idx + 1]), "wb") as f:
                f.write(data)
                f.flush()
                f.close()

            print("--- COMPILE SUCCESSFULLY ---")
