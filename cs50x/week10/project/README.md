# Genshin Artifact Database

#### Video Demo:  https://youtu.be/3UnEwEhmAMU

#### Description:

My project the 'Artifact Database' is a character statistic calculator for a game called Genshin Impact. In the game each character has stats calculated from a combination of character base stats, weapon stats and item stats. In order to create this calculator I have to allow the user to select from all the different variables in order to get an accurate final figure. In order to allow the user to more easily calculate their characters stats I felt it appropriate to allow them to submit their character items known as 'artifacts' to a database. This way they could pick and choose between all their submitted artifacts without having to enter the details each time.

For the base of the project I decided to use parts of the CS50 Finance problem set and Flask as it seemed appropriate to store and pass values to the page.

##### REGISTER & LOGIN.HTML

I started by allowing the user to register and login to the website using 'register.html' and 'login.html'.
Layout.html would always show a login screen initially but once registed and logged in it would show the last five artifacts that the user had entered into the database.


##### ACCOUNT and LOGOUT.HTML

Logout simply ends the user session

Account allows the user to delete their account and all associated artifacts. It requires a double password confirmation.

I considered implementing a password change but felt as a feature it wouldn't teach me anything new.

From there the user can select three primary options, Submit, Artifacts, Loadout.

##### SUBMIT.HTML

Users would use this page to enter artifacts into the database for future use. They would be presented with a single select menu from which to chose from. I wanted to limit their initial choices to the specific item 'slot' the artifact used as each slot would have different stats assigned to it.

There is an 'onchange' trigger for the 'change()' function which would reveal the next set of options and depending on the option chosen in the first select menu limit the options of the subsequent 'main stat' select menu that follows. The values for the 'main stat' select menu are stored in 'const slot_stats' and if the item is a 'goblet' [goblet_check()] with a 'elemental damage' stat it would show another select menu with further options [elements()].

Each item has four substats which are manually chosen and values entered by the user. In app.py checks to make sure that each substat is different and that for some slots the substat cannot be the same as the mainstat.

Finally while not used later in the website I have a menu to pick the 'set' that the artifacts come from. As this was the first page I made I experemited with passing database values to javascript using Jinja. In this case at the top of app.py I have a dict called supported_artifact_sets which stores all the values.

At the bottom of the page are two divs that pass back error or confirmation text after the user submits data.


##### ARTIFACTS.HTML

This template shows the user all the artifacts that they have entered into the database. I added the ability to sort by column and delete individual artifacts.

In order to make it more interactive I added a sort function at the top of each column. I orignally thought about sending a db request but found you could sort using javascript. From this point on I used a lot more javascript in my project. I also had to write [percentadd()] to make sure that each stat which was a percentage was properly marked.

Next to each row is a delete button. Each artifact line is made using a jinja loop with the delete button I replaced the value of each button made to the item Id.

##### LOADOUT.HTML

The largest part of the project. This is where the user can finalise their character stats.

The data used for this page is held in Javascript arrays. All user artifacts are loaded on and the [subperadd()] function adds % next to any relevant stat.

It begins by requiring the user to select one of the supported characters. For now I have provided two but others can be added into the database. This is the only "POST" request on the page as once a character is selected all other data is handled with Javascript. App.py returns the character data.

At this point since a character has been selected [addimage()] would pull up the character portrait of the selected character. The function checks if the user has selected a character and reveals the stat table.

[show()] function is how I changed the various html properties on the page as parts of it open up. It is inside [addimage()] and where the user selects a character level.

 The user must then select a level for the character so that its base stats are applied onto the adjacent table.

Then depending on the character a list of weapons is generated which can be adjusted by adding more entries into the database.

Users can then select a item for each slot from their stored artifacts which will appear adjacent to each button.

Stats are recalculated whenever a artifact is selected, weapon selected, level selected using function [stat_update()]. The function takes character base stats (level dependant). Then if a level has been selected it sets the base values into the stat table. Characters have unique modifieds so that is checked as well. I only provided support for two characters but the function could be easily expanded.

Weapon data is only updated if a level has already been selected. Artifact data just requires a level to be selected. This is so the modifiers always have a starting value (the characters base stats) to calculate from.

For the artifacts, stats are calculated by checking all the artifact stat tables and updating variables. I wasn't sure if this was the best method as each variable is essentially repeated code, but also unsure if you can store a variable name within an array to turn the process into a loop.

##### Extra

When it came to adding in artifact data enmasse instead of individually entering each artifact using submit I instead created **testcsv.csv** and a small python program **dbinsert_cartifacts.py** which I took from the cs50 sql lecture.
I also did the same for the two characters and weapons in the program. **weapons.csv** and the two **char{xxx}.csv** files.
If while testing the program I would delete all the artifacts for a user I could easily reenter them into the database again/ y