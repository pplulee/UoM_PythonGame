# The resolution of game window is 1600*900
# Other information and introduction are in README

import json
import random
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Config:
    def __init__(self):
        configfile = open("config.json", "r")
        self.configdata = json.loads(configfile.read())
        configfile.close()
        self.canvassize = [1600, 800]

    def saveconfig(self):
        # write file
        configfile = open("config.json", "w")
        configfile.write(json.dumps(self.configdata, indent=4, separators=(',', ':')))
        configfile.close()

    def setting(self):
        def save():
            self.configdata["bgcolor"] = entry_bg.get()
            self.configdata["key_up"] = entry_keyup.get()
            self.configdata["key_down"] = entry_keydown.get()
            self.configdata["key_left"] = entry_keyleft.get()
            self.configdata["key_right"] = entry_keyright.get()
            self.configdata["bosskey"] = entry_bosskey.get()
            self.configdata["move_speed"] = int(entry_movespeed.get())
            self.saveconfig()
            tk.messagebox.showinfo("Notice", "Saved successfully!")
            settingwindow.destroy()  # destroy the window

        settingwindow = tk.Tk()
        settingwindow.title("Game settings")
        settingwindow.geometry("300x300")
        label_bg = tk.Label(settingwindow, text="Background color").place(x=0, y=20, anchor="w")
        label_keyup = tk.Label(settingwindow, text="Key Up").place(x=0, y=50, anchor="w")
        label_keydown = tk.Label(settingwindow, text="Key down").place(x=0, y=80, anchor="w")
        label_keyright = tk.Label(settingwindow, text="Key Right").place(x=0, y=110, anchor="w")
        label_keyleft = tk.Label(settingwindow, text="Key Left").place(x=0, y=140, anchor="w")
        label_bosskey = tk.Label(settingwindow, text="Boss Key").place(x=0, y=170, anchor="w")
        label_movespeed = tk.Label(settingwindow, text="Move Speed").place(x=0, y=200, anchor="w")

        entry_bg = tk.Entry(settingwindow)
        entry_keyup = tk.Entry(settingwindow)
        entry_keydown = tk.Entry(settingwindow)
        entry_keyright = tk.Entry(settingwindow)
        entry_keyleft = tk.Entry(settingwindow)
        entry_bosskey = tk.Entry(settingwindow)
        entry_movespeed = tk.Entry(settingwindow)

        entry_bg.insert(0, self.configdata["bgcolor"])
        entry_keyup.insert(0, self.configdata["key_up"])
        entry_keydown.insert(0, self.configdata["key_down"])
        entry_keyright.insert(0, self.configdata["key_right"])
        entry_keyleft.insert(0, self.configdata["key_left"])
        entry_bosskey.insert(0, self.configdata["bosskey"])
        entry_movespeed.insert(0, self.configdata["move_speed"])

        entry_bg.place(x=300, y=20, anchor="e")
        entry_keyup.place(x=300, y=50, anchor="e")
        entry_keydown.place(x=300, y=80, anchor="e")
        entry_keyright.place(x=300, y=110, anchor="e")
        entry_keyleft.place(x=300, y=140, anchor="e")
        entry_bosskey.place(x=300, y=170, anchor="e")
        entry_movespeed.place(x=300, y=200, anchor="e")

        button_save = tk.Button(settingwindow, text="Save", command=save).place(x=100, y=250, anchor="n")
        button_close = tk.Button(settingwindow, text="Close", command=settingwindow.destroy).place(x=200, y=250,
                                                                                                   anchor="n")


class Leaderboard:
    def __init__(self):
        self.leaderboard = []
        file = open("leaderboard.txt", "r")
        for line in file:
            if line.rstrip() == "":  # empty line
                continue
            # username, score, date
            data = line.rstrip().split(",")
            self.leaderboard.append([data[0], int(data[1]), data[2]])
        self.leaderboard = sorted(self.leaderboard, key=lambda item: item[1], reverse=True)

    def addrecord(self, name, score):
        text = ""
        if self.getscore(name) == 0:
            # user not recorded
            self.leaderboard.append([name, int(score), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())])
        else:
            for item in self.leaderboard:
                if item[0] == name:
                    # user exists
                    item[1] = score
                    item[2] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file = open("leaderboard.txt", "w")
        for item in self.leaderboard:
            text += f"{item[0]},{item[1]},{item[2]}\n"
        file.write(text)
        file.close()

    def getscore(self, name):
        for item in self.leaderboard:
            if item[0] == name:
                return int(item[1])
        # user not found
        return 0

    def displayboard(self):
        boardwindow = tk.Tk()
        boardwindow.title("Leader Board")
        boardwindow.geometry("450x400")
        board = ttk.Treeview(boardwindow, columns=["Name", "Score", "Date"], show="headings")
        board.column("Name", width=200, anchor="center")
        board.column("Score", width=50, anchor="center")
        board.column("Date", width=200, anchor="center")
        board.heading("Name", text="Name")
        board.heading("Score", text="Score")
        board.heading("Date", text="Date")
        for i in range(0, len(self.leaderboard)):
            board.insert(index=i, values=(self.leaderboard[i]), parent='')
        board.grid()


config = Config()
leaderboard = Leaderboard()


def help():
    helpwindow = tk.Tk()
    helpwindow.title("Game tips")
    helpwindow.geometry("550x200")
    helpinfo = 'The configuration of game is in "config.json", where you can change setting if you want.\n' \
               'Current setting:\n' \
               f'UP: {config.configdata["key_up"]} DOWN: {config.configdata["key_down"]} LEFT: {config.configdata["key_left"]} RIGHT: {config.configdata["key_right"]} BOSSKEY: {config.configdata["bosskey"]}\n\n' \
               'In this game, you will play a role as a cat, and you need to eat fish on screen.\n' \
               'Everytime when you eat a fish, you will get 1 point\n' \
               'You can’t touch the edge or the road you have walked.\n' \
               'If you hit that, the game is over.\n'
    helplabel = tk.Label(helpwindow, text=helpinfo)
    helplabel.pack()


def initialise_window():
    print("Welcome!")
    mainwindow.title("Eat fish")
    mainwindow.geometry("1600x900")

    global Label_Gametitle
    Label_Gametitle = tk.Label(mainwindow, text="Eat fish game", bg="#99CCFF", font="Arial 32", width=20, height=5)
    Label_Gametitle.pack()

    global Button_Play
    Button_Play = tk.Button(mainwindow, text="Start", width=10, height=2, command=startgame)
    global Button_Exit
    Button_Exit = tk.Button(mainwindow, text="Exit", width=10, height=2, command=exit)

    global Button_Help
    global Image_Help
    Image_Help = tk.PhotoImage(file="images/Button-Help-icon.png")
    Button_Help = tk.Button(mainwindow, image=Image_Help, text="Help", command=help)

    global Button_LB  # leaderboard
    Button_LB = tk.Button(mainwindow, text="Leader Board", width=12, height=2, command=leaderboard.displayboard)

    global Button_config  # setting interface
    global Image_config
    Image_config = tk.PhotoImage(file="images/settings-icon.png")
    Button_config = tk.Button(mainwindow, text="Setting", image=Image_config, command=config.setting)

    Button_Play.place(x=700, y=350, anchor="center")
    Button_Exit.place(x=900, y=350, anchor="center")
    Button_Help.place(x=800, y=350, anchor="center")
    Button_LB.place(x=800, y=450, anchor="center")
    Button_config.place(x=800, y=550, anchor="center")

    global Username
    Username = "anonymous"  # set default user name

    global Label_Nameinput
    Label_Nameinput = tk.Label(mainwindow, text="Your user name:", font="Arial 12")
    Label_Nameinput.place(x=720, y=280, anchor="e")
    global NameInput
    NameInput = tk.Entry(mainwindow)
    NameInput.place(x=800, y=280, anchor="center")

    global Label_Author
    Label_Author = tk.Label(mainwindow, text="Developer: Ziyi Li", font="Arial 12", width=20, height=5)
    Label_Author.place(x=800, y=800, anchor="center")

    global GameCanvas
    GameCanvas = tk.Canvas(mainwindow, width=config.canvassize[0], height=config.canvassize[1],
                           bg=config.configdata["bgcolor"])

    mainwindow.focus_set()
    mainwindow.bind(f"<KeyPress-{config.configdata['bosskey']}>", bosskey)


def bosskey(event):
    global mainwindow
    global GameCanvas
    mainwindow.withdraw()  # hide the main window
    while input("Enter Y is you want to back yo game") != "Y":
        continue
    mainwindow.update()
    mainwindow.deiconify()
    GameCanvas.focus_set()


def game_end():
    # print("game over") # use for debug
    global alive
    alive = False
    global Label_Gameover
    Label_Gameover = tk.Label(mainwindow, text="Game over", bg="#f57b42", font="Arial 30", width=10, height=2)
    Label_Gameover.place(x=800, y=900, anchor="s")
    global point
    global Username
    if leaderboard.getscore(Username) < point:
        leaderboard.addrecord(Username, point)
        tk.messagebox.showinfo("Congratulations!", "You got a new high score")


def game_restart():
    global GameCanvas
    global Label_Gameover
    GameCanvas.delete("all")  # delete all elements on canvas
    Label_Gameover.place_forget()
    startgame()


def startgame():
    global config

    def CheckPos(pos):
        # detect it character hit the edge, or hit the trajectory
        if (pos in Trajectory) or (pos[0] <= 0) or (pos[0] >= config.canvassize[0]) or (pos[1] <= 0) or (
                pos[1] >= config.canvassize[1]):
            # print("ji") # use for debug
            game_end()
            return False
        else:
            return True

    def HitDetect(pos):
        global point
        scope = 20
        fishpos = GameCanvas.coords(Fish)
        if (pos[0] - scope < fishpos[0] < pos[0] + scope) and (pos[1] - scope < fishpos[1] < pos[1] + scope):
            # hit the fish
            point += 1
            UpdateFish()
            GameScoreboard[0].config(text=f"Score: {point}")
            GameScoreboard[0].update()

    def Move(direction):
        global distance
        global GameCanvas
        distance += config.configdata["move_speed"]
        Trajectory.append(GameCanvas.coords(GameCharacter))
        if alive:
            if direction == "up":
                GameCanvas.create_line(GameCanvas.coords(GameCharacter), GameCanvas.coords(GameCharacter)[0],
                                       GameCanvas.coords(GameCharacter)[1] - config.configdata["move_speed"])
                GameCanvas.move(GameCharacter, 0, -config.configdata["move_speed"])
            elif direction == "left":
                GameCanvas.create_line(GameCanvas.coords(GameCharacter),
                                       GameCanvas.coords(GameCharacter)[0] - config.configdata["move_speed"],
                                       GameCanvas.coords(GameCharacter)[1])
                GameCanvas.move(GameCharacter, -config.configdata["move_speed"], 0)
            elif direction == "down":
                GameCanvas.create_line(GameCanvas.coords(GameCharacter), GameCanvas.coords(GameCharacter)[0],
                                       GameCanvas.coords(GameCharacter)[1] + config.configdata["move_speed"])
                GameCanvas.move(GameCharacter, 0, config.configdata["move_speed"])
            elif direction == "right":
                GameCanvas.create_line(GameCanvas.coords(GameCharacter),
                                       GameCanvas.coords(GameCharacter)[0] + config.configdata["move_speed"],
                                       GameCanvas.coords(GameCharacter)[1])
                GameCanvas.move(GameCharacter, config.configdata["move_speed"], 0)
            GameScoreboard[1].config(text=f"Distance: {distance}")
            GameScoreboard[1].update()
            CheckPos(GameCanvas.coords(GameCharacter))
            HitDetect(GameCanvas.coords(GameCharacter))

    def generatefishpos():
        safe_distance = 30
        pos = [random.randint(safe_distance, config.canvassize[0] - safe_distance),
               random.randint(safe_distance, config.canvassize[1] - safe_distance)]
        if pos in Trajectory:  # pos on trajectory
            return generatefishpos()
        for i in Trajectory:  # pos is close to trajectory
            if (i[0] - safe_distance < pos[0] < i[1] + safe_distance) and (
                    i[1] - safe_distance < pos[1] < i[1] + safe_distance):
                return generatefishpos()
        return pos

    def UpdateFish():
        GameCanvas.coords(Fish, generatefishpos())
        # print(GameCanvas.coords(Fish)) # use for debug

    def keyevent(event):
        # handle key event
        # print(event.char) # use for debug
        global point
        if event.char == config.configdata["key_up"]:
            Move("up")
        elif event.char == config.configdata["key_left"]:
            Move("left")
        elif event.char == config.configdata["key_down"]:
            Move("down")
        elif event.char == config.configdata["key_right"]:
            Move("right")
        elif event.char == "+":
            point += 1  # cheat code
            GameScoreboard[0].config(text=f"Score: {point}")
            GameScoreboard[0].update()
        elif event.char == "-":
            point -= 1  # cheat code
            GameScoreboard[0].config(text=f"Score: {point}")
            GameScoreboard[0].update()

    # Hide elements on previous interface
    Label_Gametitle.pack_forget()
    Button_Play.place_forget()
    Button_Help.place_forget()
    Button_LB.place_forget()
    Button_config.place_forget()
    Label_Author.place_forget()
    Label_Nameinput.place_forget()
    global NameInput
    NameInput.place_forget()

    global point
    point = 0
    global distance
    distance = 0
    global alive
    alive = True

    global GameCanvas
    global Username

    if NameInput.get() != "":
        Username = NameInput.get()

    Trajectory = []  # list to store the trajectory

    GameCharacter_File = tk.PhotoImage(file="images/cat.png")
    GameCharacter = GameCanvas.create_image(0, 0, anchor="center", image=GameCharacter_File)
    GameCanvas.coords(GameCharacter, 800, 400)

    Fish_File = tk.PhotoImage(file="images/fish.png")
    Fish = GameCanvas.create_image(generatefishpos(), anchor="center", image=Fish_File)

    Button_Restart = tk.Button(mainwindow, text="Restart", width=10, height=2, command=game_restart)
    Button_Restart.place(x=1200, y=900, anchor="s")
    Button_Exit.place(x=1300, y=900, anchor="s")

    GameCanvas.focus_set()
    GameCanvas.bind("<Key>", keyevent)
    GameCanvas.pack()

    GameScoreboard = [None, None, None]  # 0 - Points,1 - Distance,2 - Best Score
    GameScoreboard[0] = tk.Label(mainwindow, text=f"Score: {point}", bg="#CCFF99", font="Arial 15", width=15, height=4)
    GameScoreboard[1] = tk.Label(mainwindow, text=f"Distance: {distance}", bg="#FFCC99", font="Arial 15", width=15,
                                 height=4)
    GameScoreboard[2] = tk.Label(mainwindow, text=f"Best Score: {leaderboard.getscore(Username)}", font="Arial 10")
    GameScoreboard[0].place(x=0, y=900, anchor="sw")
    GameScoreboard[1].place(x=1600, y=900, anchor="se")
    GameScoreboard[2].place(x=250, y=900, anchor="s")
    GameCanvas.update()
    mainwindow.mainloop()


mainwindow = tk.Tk()
initialise_window()

mainwindow.mainloop()
