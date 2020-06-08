#!/bin/bash
# zip the game
cd app
zip -r ../Platformer.zip *
cd ..

# create executable from zip
echo '#!/usr/bin/env python' | cat - Platformer.zip > Game
echo '#!/usr/bin/env python3' | cat - Platformer.zip > Game
chmod a+x Game

# run the game
./Game