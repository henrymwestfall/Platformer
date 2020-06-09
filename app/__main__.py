import sys
import os

def main():
    g = Game()
    g.start()

if __name__ == "__main__":
    tasks = [
        lambda: os.system("pip install pygame"),
        lambda: os.system("pip3 install pygame"),
    ]
    for t in tasks:
        try:
            import pygame
            break
        except ImportError:
            t()
    else:
        print("Error: Failed to install pygame. Opening pygame.org in browser.")
        import webbrowser
        webbrowser.open("https://www.pygame.org/wiki/GettingStarted", new=2)
        sys.exit()
    print("pygame successfully imported!")

    from game import Game
    os.system("exit")
    main()
