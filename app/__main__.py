import sys
import os

from game import Game

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
        print("Error: Failed to install pygame.")
        sys.exit()
    print("pygame successfully imported")
    main()
