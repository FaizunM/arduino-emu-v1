from application.pages.monitor import MonitorWindow
from application.pages.flash import FlashWindow
from application.pages.SRAM import SRAMWindow
from application.pages.eeprom import EEPROMWindow
from application.pages.registers import RegisterWindow


class PageManager:
    def __init__(self, stdscr, PC, flash, SRAM, EEPROM, ins_register):
        self.PC = PC
        self.flash = flash
        self.SRAM = SRAM
        self.EEPROM = EEPROM
        self.ins_register = ins_register

        self.stdscr = stdscr
        self.height, self.width = self.stdscr.getmaxyx()

        self.pages = [
            MonitorWindow(self.height - 4, self.width, 3, 0, self.PC, self.flash),
            SRAMWindow(self.height - 4, self.width, 3, 0, self.SRAM),
            EEPROMWindow(self.height - 4, self.width, 3, 0, self.EEPROM),
            FlashWindow(self.height - 4, self.width, 3, 0, self.flash),
            RegisterWindow(self.height - 4, self.width, 3, 0, self.ins_register),
        ]
        self.current_index = 0
        self.show_header = False
        
        for page in self.pages:
            page.window.resize(self.height - 1, self.width)
            page.window.mvwin(0, 0)
            page.height = self.height - 2

    def draw(self):
        self.pages[self.current_index].draw()

    def handle_input(self, key):
        if key == ord("h"):
            if not self.show_header:
                self.pages[self.current_index].window.resize(
                    self.height - 4, self.width
                )
                self.pages[self.current_index].window.mvwin(3, 0)
                self.pages[self.current_index].height = self.height - 5
                self.show_header = True
            else:
                self.pages[self.current_index].window.resize(
                    self.height - 1, self.width
                )
                self.pages[self.current_index].window.mvwin(0, 0)
                self.pages[self.current_index].height = self.height - 2
                self.show_header = False

        handled = self.pages[self.current_index].handle_input(key)
        return handled
