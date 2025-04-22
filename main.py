from application.app import MyApplication
import curses

def main(stdscr):
    app = MyApplication(stdscr)
    app.run()
    
if __name__ == "__main__":
    curses.wrapper(main)
