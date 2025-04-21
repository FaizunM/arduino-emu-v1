from core.instructions.instruction_register import InstructionRegister
from core.alu import ALU
from core.program_counter import ProgramCounter
from core.memory.sram import SRAM
from core.memory.flash import Flash
from core.memory.eeprom import EEPROM
from application.hex_dump import HexDump
from application.monitor import Monitor
import os


class MainApp:
    def __init__(self):
        self.ins_register = InstructionRegister()
        self.flash = Flash()
        self.SRAM = SRAM()
        self.PC = ProgramCounter(self.flash, self.ins_register, self.SRAM)
        self.EEPROM = EEPROM()

    def read_SRAM(self):
        self.header()
        print("\n --- SRAM READER ---\n")
        dump = HexDump(self.SRAM.memory)
        start = format(0, "X").zfill(4)
        end = format(len(self.SRAM.memory) - 1, "X").zfill(4)
        print(f"\n --- {start}:{end} ---")
        address = input(" Address <start:end> --> ")
        split = address.split(":")
        dump.dumpv2(int(split[0], 16), int(split[1], 16))

        self.bottom_bar(self.read_SRAM)

    def read_flash(self):
        self.header()
        print("\n --- Flash READER ---\n")
        dump = HexDump(self.flash.memory)
        start = format(0, "X").zfill(4)
        end = format(len(self.flash.memory) - 1, "X").zfill(4)
        print(f"\n --- {start}:{end} ---")
        address = input(" Address <start:end> --> ")
        split = address.split(":")
        dump.dumpv2(int(split[0], 16), int(split[1], 16))

        self.bottom_bar(self.read_flash)

    def read_EEPROM(self):
        self.header()
        print("\n --- EEPROM READER ---\n")

        dump = HexDump(self.EEPROM.memory)
        start = format(0, "X").zfill(4)
        end = format(len(self.EEPROM.memory) - 1, "X").zfill(4)
        print(f"\n --- {start}:{end} ---")
        address = input(" Address <start:end> --> ")
        split = address.split(":")
        dump.dumpv2(int(split[0], 16), int(split[1], 16))

        self.bottom_bar(self.read_EEPROM)

    def read_registers(self):
        self.header()
        print("\n --- Registers READER ---\n")

        dump = HexDump(self.ins_register.registers)
        dump.dumpv2(0, len(self.ins_register.registers))

        self.bottom_bar(self.read_registers)

    def bottom_bar(self, refresh, with_clock=False):
        if with_clock:
            text = f"\n[Enter] Cycle the PC [B] Back --> "
        else:
            text = f"\n[Enter] Refresh [B] Back --> "
            
        option = input(text)
        if option.lower() == "b":
            return
        else:
            if with_clock:
                self.PC.cycle()
            refresh()

    def monitor(self):
        self.header()
        print("\n --- MONITOR ---\n")
        
        monitor = Monitor(self.flash, self.PC)
        monitor.show()

        self.bottom_bar(self.monitor, True)

    def header(self):
        os.system("clear")
        print(
            f"""______________________________________________________________
           _____  _____  _    _        ______ __  __ _    _ 
     /\   |  __ \|  __ \| |  | |      |  ____|  \/  | |  | |
    /  \  | |__) | |  | | |  | |______| |__  | \  / | |  | |
   / /\ \ |  _  /| |  | | |  | |______|  __| | |\/| | |  | |
  / ____ \| | \ \| |__| | |__| |      | |____| |  | | |__| |
 /_/    \_\_|  \_\_____/ \____/       |______|_|  |_|\____/ 
 
 Program Counter -> 0x{format(self.PC.address, 'X').zfill(8)}
______________________________________________________________
"""
        )

    def run(self):
        while True:
            self.header()

            print("--- MENU ---")
            menus = [
                {"text": "Monitor", "command": self.monitor},
                {"text": "Read Flash", "command": self.read_flash},
                {"text": "Read SRAM", "command": self.read_SRAM},
                {"text": "Read EEPROM", "command": self.read_EEPROM},
                {"text": "Read Registers", "command": self.read_registers},
            ]
            for idx, menu in enumerate(menus):
                print(f"[ {idx+1} ] {menu['text']}")
            select = input("\n--- Select -> ")
            menus[int(select) - 1]["command"]()
