import requests
from bs4 import BeautifulSoup, Comment, SoupStrainer
from collections import defaultdict

class Player:
    def __init__(self, name):
        self.name = name
        self.fgs = []
        self.fgm = 0
        self.fga = 0
        self.jumpfgs = []
        self.jumpfgm = 0
        self.jumpfga = 0
        self.threefgs = []
        self.threefgm = 0
        self.threefga = 0

    def __str__(self):
        return self.name + str(self.fgm) + "/" + str(self.fga) + str(self.fgs)

    def fg(self, result):
        self.fgs.append(result)
        self.fga = self.fga + 1
        if result:
            self.fgm = self.fgm + 1
    def jumpfg(self, result):
        self.jumpfgs.append(result)
        self.jumpfga = self.jumpfga + 1
        if result:
            self.jumpfgm = self.jumpfgm + 1
    def threefg(self, result):
        self.threefgs.append(result)
        self.threefga = self.threefga + 1
        if result:
            self.threefgm = self.threefgm + 1
    def game_end(self):
        self.fgs.append(0)
        self.jumpfgs.append(0)
        self.threefgs.append(0)

    def analyze(self, write):
        shotlists = [self.fgs, self.jumpfgs, self.threefgs]
        pershot_fgp = {}
        cur_streak = 0
        which_list = 0
        for shot_list in shotlists:
            for shot in shot_list:
                if type(shot) == int:
                    cur_streak = 0
                
                else:
                    if cur_streak not in pershot_fgp:
                        pershot_fgp[cur_streak] = (0,0)
                    if shot:
                        made, attempted = pershot_fgp[cur_streak]
                        pershot_fgp[cur_streak] = made+1, attempted+1
                        cur_streak = cur_streak + 1
                    else:
                        made, attempted = pershot_fgp[cur_streak]
                        pershot_fgp[cur_streak] = made, attempted+1
                        cur_streak = 0
            for streak in pershot_fgp:
                made, attempted = pershot_fgp[streak]
                pershot_fgp[streak] = float(made)/attempted

            if which_list == 0:
                if self.fga > 0:
                    fgp = float(self.fgm)/self.fga
                else:
                    #This foool only took free throws
                    fgp = 0
                write.write(self.name + " All FG%: " + str(round(fgp,2))+ '\n')
                
            elif which_list == 1:
                if self.jumpfga >=175:
                    fgp = float(self.jumpfgm)/self.jumpfga
                    write.write(self.name + " Jump Shot FG%: " + str(round(fgp,2))+'\n')
                else:
                    write.write("DID Not shoot 175 Jumpshots \n")
            elif which_list == 2:
                if self.threefga >= 150:
                    fgp = float(self.threefgm)/self.threefga
                    write.write(self.name + " 3FG%: " + str(round(fgp,2))+'\n')
                else:
                    write.write("DID NOT SHoot 150 jumpshots\n")
            write.write(str(pershot_fgp) + '\n')
            pershot_fgp = {}
            which_list = which_list + 1
        print('\n')

def game(URL_ending, playernames):
    res = requests.get("https://www.basketball-reference.com/boxscores/pbp/"+URL_ending+".html",headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(res.text, 'lxml', parse_only=SoupStrainer(id = 'pbp'))
    
    

    for box in soup.find_all('td'):
        if len(box.text) == 0:
            box.extract()


    for box in soup.find_all('td'):
        if "makes" not in box.text:
            if "misses" not in box.text:
                if "from" not in box.text:
                    box.extract()


    cur_players = []
    last_result = ""
    for link in soup.find_all('a'): 
        shot_result = link.find_parent().text
        cur_player = 0
        if link.text not in cur_players:
            cur_players.append(link.text)
        if link.text not in playernames:
            cur_player = Player(link.text)
            playernames[link.text] = cur_player
        else:
            cur_player = playernames[link.text]
        if shot_result != last_result:
            if "from" in shot_result or 'at rim' in shot_result:
                cur_player.fg("makes" in shot_result)
                if "layup" not in shot_result and "dunk" not in shot_result:
                    cur_player.jumpfg("makes" in shot_result)
                    if "3-pt" in shot_result:
                        cur_player.threefg("makes" in shot_result)
        last_result = shot_result
    for player in cur_players:
        cur_player = playernames[player]
        cur_player.game_end()



URL_endings = []
with open('games_URLS.txt') as fp:
    for line in fp:
        line = line[:-1]
        URL_endings.append(line)

fp.close()

playernames = {}
i = 0
length  = len(URL_endings)
for URL in URL_endings:
    game(URL, playernames)
    i = i + 1
    print("Game " + str(i) + " of" + str(length))

i = 0
length = len(playernames)
write = open("2018PlayerDataComparison.txt", "w+")

for player in iter(playernames.values()):
    if player.fga >= 450:
        player.analyze(write)
    i = i + 1
    print("Player " + str(i) + " of" + str(length))

write.close()
