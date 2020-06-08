:: zip the game
cd app
for /d %%a in (*) do (zip -r -p "%%..\Platformer.zip" ".\%%a\*")
cd ..

:: create an executable from the zip


:: run the game