import requests
import os
import re

movie_barcodes = [
    ("2001 - A Space Odyssey", "https://zerowidthjoiner.net/uploads/movie-barcodes/2001%20-%20A%20Space%20Odyssey.png"),
    ("300", "https://zerowidthjoiner.net/uploads/movie-barcodes/300.png"),
    ("500 Days of Summer", "https://zerowidthjoiner.net/uploads/movie-barcodes/500%20Days%20of%20Summer.png"),
    ("Akira", "https://zerowidthjoiner.net/uploads/movie-barcodes/Akira.png"),
    ("Annihilation", "https://zerowidthjoiner.net/uploads/movie-barcodes/Annihilation.png"),
    ("Arrival", "https://zerowidthjoiner.net/uploads/movie-barcodes/Arrival.png"),
    ("Astérix et Obélix - Mission Cléopâtre", "https://zerowidthjoiner.net/uploads/movie-barcodes/Ast%C3%A9rix%20et%20Ob%C3%A9lix%20-%20Mission%20Cl%C3%A9op%C3%A2tre.png"),
    ("Austra - The Beat And The Pulse (Music video)", "https://zerowidthjoiner.net/uploads/movie-barcodes/Austra%20-%20The%20Beat%20And%20The%20Pulse%20(Music%20video).png"),
    ("Avatar", "https://zerowidthjoiner.net/uploads/movie-barcodes/Avatar.png"),
    ("Bajirao Mastani", "https://zerowidthjoiner.net/uploads/movie-barcodes/Bajirao%20Mastani.png"),
    ("Barbarella", "https://zerowidthjoiner.net/uploads/movie-barcodes/Barbarella.png"),
    ("Beetlejuice", "https://zerowidthjoiner.net/uploads/movie-barcodes/Beetlejuice.png"),
    ("Big Trouble in Little China", "https://zerowidthjoiner.net/uploads/movie-barcodes/Big%20Trouble%20in%20Little%20China.png"),
    ("Blade Runner 2049", "https://zerowidthjoiner.net/uploads/movie-barcodes/Blade%20Runner%202049.png"),
    ("Bon Cop Bad Cop", "https://zerowidthjoiner.net/uploads/movie-barcodes/Bon%20Cop%20Bad%20Cop.png"),
    ("Cinnamon Chasers - Luv Deluxe (Music video)", "https://zerowidthjoiner.net/uploads/movie-barcodes/Cinnamon%20Chasers%20-%20Luv%20Deluxe%20(Music%20video).png"),
    ("Cloud Atlas", "https://zerowidthjoiner.net/uploads/movie-barcodes/Cloud%20Atlas.png"),
    ("Cloverfield", "https://zerowidthjoiner.net/uploads/movie-barcodes/Cloverfield.png"),
    ("Deadpool 2", "https://zerowidthjoiner.net/uploads/movie-barcodes/Deadpool%202.png"),
    ("Deftones - Sextape (Music video)", "https://zerowidthjoiner.net/uploads/movie-barcodes/Deftones%20-%20Sextape%20(Music%20video).png"),
    ("DYE - Fantasy (Music video)", "https://zerowidthjoiner.net/uploads/movie-barcodes/DYE%20-%20Fantasy%20(Music%20video).png"),
    ("God Bless America", "https://zerowidthjoiner.net/uploads/movie-barcodes/God%20Bless%20America.png"),
    ("Goliyon Ki Raasleela Ram-Leela", "https://zerowidthjoiner.net/uploads/movie-barcodes/Goliyon%20Ki%20Raasleela%20Ram-Leela.png"),
    ("Good Will Hunting", "https://zerowidthjoiner.net/uploads/movie-barcodes/Good%20Will%20Hunting.png"),
    ("Hanna", "https://zerowidthjoiner.net/uploads/movie-barcodes/Hanna.png"),
    ("iamamwhoami - y (Music video)", "https://zerowidthjoiner.net/uploads/movie-barcodes/iamamwhoami%20-%20y%20(Music%20video).png"),
    ("In Time", "https://zerowidthjoiner.net/uploads/movie-barcodes/In%20Time.png"),
    ("Inception", "https://zerowidthjoiner.net/uploads/movie-barcodes/Inception.png"),
    ("Jaws", "https://zerowidthjoiner.net/uploads/movie-barcodes/Jaws.png"),
    ("Kick Ass", "https://zerowidthjoiner.net/uploads/movie-barcodes/Kick%20Ass.png"),
    ("La Cité de la Peur", "https://zerowidthjoiner.net/uploads/movie-barcodes/La%20Cit%C3%A9%20de%20la%20Peur.png"),
    ("Love Death and Robots s01e01 Sonnies Edge", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e01%20Sonnies%20Edge.png"),
    ("Love Death and Robots s01e02 Three Robots", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e02%20Three%20Robots.png"),
    ("Love Death and Robots s01e03 The Witness", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e03%20The%20Witness.png"),
    ("Love Death and Robots s01e04 Suits", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e04%20Suits.png"),
    ("Love Death and Robots s01e05 Sucker of Souls", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e05%20Sucker%20of%20Souls.png"),
    ("Love Death and Robots s01e06 When the Yogurt Took Over", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e06%20When%20the%20Yogurt%20Took%20Over.png"),
    ("Love Death and Robots s01e07 Beyond the Aquila Rift", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e07%20Beyond%20the%20Aquila%20Rift.png"),
    ("Love Death and Robots s01e08 Good Hunting", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e08%20Good%20Hunting.png"),
    ("Love Death and Robots s01e09 The Dump", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e09%20The%20Dump.png"),
    ("Love Death and Robots s01e10 Shape-Shifters", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e10%20Shape-Shifters.png"),
    ("Love Death and Robots s01e11 Helping Hand", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e11%20Helping%20Hand.png"),
    ("Love Death and Robots s01e12 Fish Night", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e12%20Fish%20Night.png"),
    ("Love Death and Robots s01e13 Lucky 13", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e13%20Lucky%2013.png"),
    ("Love Death and Robots s01e14 Zima Blue", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e14%20Zima%20Blue.png"),
    ("Love Death and Robots s01e15 Blindspot", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e15%20Blindspot.png"),
    ("Love Death and Robots s01e16 Ice Age", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e16%20Ice%20Age.png"),
    ("Love Death and Robots s01e17 Alternate Histories", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e17%20Alternate%20Histories.png"),
    ("Love Death and Robots s01e18 The Secret War", "https://zerowidthjoiner.net/uploads/movie-barcodes/Love%20Death%20and%20Robots%20s01e18%20The%20Secret%20War.png"),
    ("Martha Marcy May Marlene", "https://zerowidthjoiner.net/uploads/movie-barcodes/Martha%20Marcy%20May%20Marlene.png"),
    ("Meg Myers - Desire (Music video)", "https://zerowidthjoiner.net/uploads/movie-barcodes/Meg%20Myers%20-%20Desire%20(Music%20video).png"),
    ("Mind Game", "https://zerowidthjoiner.net/uploads/movie-barcodes/Mind%20Game.png"),
    ("My Neighbor Totoro", "https://zerowidthjoiner.net/uploads/movie-barcodes/My%20Neighbor%20Totoro.png"),
    ("Pacific Rim", "https://zerowidthjoiner.net/uploads/movie-barcodes/Pacific%20Rim.png"),
    ("Pan's Labyrinth", "https://zerowidthjoiner.net/uploads/movie-barcodes/Pan%27s%20Labyrinth.png"),
    ("Paprika", "https://zerowidthjoiner.net/uploads/movie-barcodes/Paprika.png"),
    ("Paths of Hate (short)", "https://zerowidthjoiner.net/uploads/movie-barcodes/Paths%20of%20Hate%20(short).png"),
    ("Princess Mononoke", "https://zerowidthjoiner.net/uploads/movie-barcodes/Princess%20Mononoke.png"),
    ("PSY - Gangnam Style (Music video)", "https://zerowidthjoiner.net/uploads/movie-barcodes/PSY%20-%20Gangnam%20Style%20(Music%20video).png"),
    ("Riverdance - New York 96", "https://zerowidthjoiner.net/uploads/movie-barcodes/Riverdance%20-%20New%20York%2096.png"),
    ("Russ Chimes - Midnight Club (Complete Trilogy) (Music video)", "https://zerowidthjoiner.net/uploads/movie-barcodes/Russ%20Chimes%20-%20Midnight%20Club%20(Complete%20Trilogy)%20(Music%20video).png"),
    ("Scott Pilgrim vs. the World", "https://zerowidthjoiner.net/uploads/movie-barcodes/Scott%20Pilgrim%20vs.%20the%20World.png"),
    ("Sucker Punch", "https://zerowidthjoiner.net/uploads/movie-barcodes/Sucker%20Punch.png"),
    ("The Cabin in the Woods", "https://zerowidthjoiner.net/uploads/movie-barcodes/The%20Cabin%20in%20the%20Woods.png"),
    ("The Curious Case of Benjamin Button", "https://zerowidthjoiner.net/uploads/movie-barcodes/The%20Curious%20Case%20of%20Benjamin%20Button.png"),
    ("The Departed", "https://zerowidthjoiner.net/uploads/movie-barcodes/The%20Departed.png"),
    ("The Girl With The Dragon Tattoo", "https://zerowidthjoiner.net/uploads/movie-barcodes/The%20Girl%20With%20The%20Dragon%20Tattoo.png"),
    ("The Lord of the Rings 1 - The Fellowship of the Ring (Extended Version)", "https://zerowidthjoiner.net/uploads/movie-barcodes/The%20Lord%20of%20the%20Rings%201%20-%20The%20Fellowship%20of%20the%20Ring%20(Extended%20Version).png"),
    ("The Lord of the Rings 2 - The Two Towers (Extended Version)", "https://zerowidthjoiner.net/uploads/movie-barcodes/The%20Lord%20of%20the%20Rings%202%20-%20The%20Two%20Towers%20(Extended%20Version).png"),
    ("The Lord of the Rings 3 - The Return of the King (Extended Version)", "https://zerowidthjoiner.net/uploads/movie-barcodes/The%20Lord%20of%20the%20Rings%203%20-%20The%20Return%20of%20the%20King%20(Extended%20Version).png"),
    ("The Matrix 1", "https://zerowidthjoiner.net/uploads/movie-barcodes/The%20Matrix%201.png"),
    ("The Matrix 2 - Reloaded", "https://zerowidthjoiner.net/uploads/movie-barcodes/The%20Matrix%202%20-%20Reloaded.png"),
    ("The Matrix 3 - Revolutions", "https://zerowidthjoiner.net/uploads/movie-barcodes/The%20Matrix%203%20-%20Revolutions.png"),
    ("The Princess Bride", "https://zerowidthjoiner.net/uploads/movie-barcodes/The%20Princess%20Bride.png"),
    ("The Sky Crawlers", "https://zerowidthjoiner.net/uploads/movie-barcodes/The%20Sky%20Crawlers.png"),
    ("The Spirit", "https://zerowidthjoiner.net/uploads/movie-barcodes/The%20Spirit.png"),
    ("Tucker & Dale vs. Evil", "https://zerowidthjoiner.net/uploads/movie-barcodes/Tucker%20&%20Dale%20vs.%20Evil.png"),
    ("Unbreakable", "https://zerowidthjoiner.net/uploads/movie-barcodes/Unbreakable.png"),
    ("Zombieland", "https://zerowidthjoiner.net/uploads/movie-barcodes/Zombieland.png"),
]

def sanitize_filename(name):
    # Remove or replace characters that are invalid in filenames
    return re.sub(r'[\\/*?\":<>|]', "_", name)

os.makedirs("movie_barcodes", exist_ok=True)

for name, url in movie_barcodes:
    filename = f"movie_barcodes/{sanitize_filename(name)}.png"
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Failed to download {name}: {e}")
