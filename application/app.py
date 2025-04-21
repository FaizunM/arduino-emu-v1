from core.instructions.instruction_register import InstructionRegister
from core.program_counter import ProgramCounter
from core.memory.sram import SRAM
from core.memory.flash import Flash
from core.memory.eeprom import EEPROM
from application.page_manager import PageManager
import curses


class MyApplication:
    def __init__(self, stdscr):
        self.ins_register = InstructionRegister()
        self.flash = Flash()
        self.SRAM = SRAM()
        self.PC = ProgramCounter(self.flash, self.ins_register, self.SRAM)
        self.EEPROM = EEPROM()

        self.stdscr = stdscr
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.keypad(True)
        self.running = True
        self.pos_y = 0
        self.pos_x = 0
        self.height, self.width = self.stdscr.getmaxyx()

        self.page_manager = PageManager(
            self.stdscr, self.PC, self.flash, self.SRAM, self.EEPROM
        )

    def draw_bottom_bar(self):
        self.stdscr.addstr(self.height - 1, 0, " " * (self.width - 1), curses.A_REVERSE)
        self.stdscr.addstr(
            self.height - 1,
            0,
            "F1 - Monitor    F2 - Flash Tab     F3 - SRAM Tab   F4 - EEPROM Tab   F5 - Registers Tab",
            curses.A_REVERSE,
        )

    def draw(self):
        self.stdscr.erase()
        self.stdscr.addstr(0, 1, f"PC Address ->  {hex(self.PC.address)} ")
        self.stdscr.addstr(1, 1, f"Flash Used ->  [")
        self.stdscr.addstr(
            1,
            18,
            " "
            * int((self.flash.get_used()["percent"] / 100) * ((self.width // 2) - 20)),
            curses.A_REVERSE,
        )
        self.stdscr.addstr(1, (self.width // 2) - 2, "]")
        self.stdscr.addstr(
            1,
            (self.width // 2) - 35,
            f"{self.flash.get_used()['percent']:.2f}% - [ 0x0 - {hex(self.flash.get_used()['end'])} ]",
        )
        self.stdscr.addstr(
            2,
            1,
            f"On Process ->  {format(self.flash.get(self.PC.address), 'b').zfill(32)} ",
        )
        self.draw_bottom_bar()
        self.stdscr.noutrefresh()
        self.page_manager.draw()

        curses.doupdate()

    def handle_input(self):
        key = self.stdscr.getch()
        handled = self.page_manager.handle_input(key)

        if not handled:
            if key == ord("q"):
                self.running = False
            elif key == curses.KEY_RIGHT:
                self.page_manager.current_index = (
                    self.page_manager.current_index + 1
                ) % len(self.page_manager.pages)
            elif key == curses.KEY_LEFT:
                self.page_manager.current_index = (
                    self.page_manager.current_index - 1
                ) % len(self.page_manager.pages)

    def run(self):
        while self.running:
            self.draw()
            self.handle_input()
