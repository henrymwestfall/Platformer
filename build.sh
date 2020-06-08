#!/bin/bash
# zip the game
cd app
zip -r ../Platformer.zip *
cd ..

# create executable from zip
echo '#!/usr/bin/env python' | cat - Platformer.zip > Game-Unix
echo '#!/usr/bin/env python3' | cat - Platformer.zip > Game-Unix
chmod a+x Game-Unix

# run the game
./Game-Unix