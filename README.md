# Constellation-Mapper
A program for mapping stars and their constellations.

### What does it do?
This program parses CSV data of star locations and size (four files provided in the star_locations folder) and draws them using the built in Python 3 Turtle module. After which you can input constellation names which will draw lines connecting the stars to form the given constellation on the map.

### How do I get it to work on my computer?

1. Run the `main.py` file in the command line or the editor/IDE of your choosing. 

2. The program will prompt you for a star location file name. I have provided four in the `star_locations` folder. Just type in "star_locations/" followed by whichever star location file you want to draw. `stars_1.dat` contains the least amount of stars and `stars_named.dat` contains the most.

  - Running the program with the names flag, `main.py -names`, will draw the stars with their name displayed above them.

  - I wouldn't recommend adding your own location files to this folder just yet as this project needs alot of work and handles input in a very rigid way. I plan on implementing a much smoother and more flexible user experience later.

3. Now the program will begin drawing the stars. Depending on your computer's processing speed and the star file chosen this could take a few minutes to finish.

4. Once all of the stars have been drawn the program will then prompt you for a constellation name. I have provided eight in the constellations folder. Just type in "constellations/" followed by the constellation you want to draw. After the constellation has been drawn it will prompt you to continue entering constellations. Simply enter nothing to quit the program. Again, just as with the star_locations folder this project handles the constellation data in a very rigid manner. So if you add your own data file to this folder it may not handle it properly.

