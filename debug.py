from application.old import MainApp
import curses

if __name__ == "__main__":
    try:
        app = MainApp()
        app.run()
    except KeyboardInterrupt:
        print("Exit by Keyboard Interrupt")

    except Exception as e:
        print(f"ERROR -> {str(e)}")
