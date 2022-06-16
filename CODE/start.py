#main run file

from gui import PayGui
from settings import Settings

def main():
    gui = PayGui()

    while(gui.shouldRespawn()):
        gui = PayGui()

    Settings.saveToFile()

if __name__ == '__main__':
    main()