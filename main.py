# The resolution of game window is 1600*900
# Other information and introduction are in README

import json
import random
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class Config:
    def __init__(self):
        configfile = open("config.json", "r")
        self.configdata = json.loads(configfile.read())
        configfile.close()
        self.canvassize = self.configdata["canvas_size"]
        self.movespeed = self.configdata["move_speed"]
        self.keyup = self.configdata["key_up"]
        self.keydown = self.configdata["key_down"]
        self.keyleft = self.configdata["key_left"]
        self.keyright = self.configdata["key_right"]
        self.bosskey = self.configdata["bosskey"]
        self.bgcolor = self.configdata["bgcolor"]


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
               f'UP:{config.keyup} DOWN:{config.keydown} LEFT:{config.keyleft} RIGHT:{config.keyright} BOSSKEY:{config.bosskey}\n\n' \
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
    Label_Gametitle = tk.Label(mainwindow, text="A simple game", bg="#99CCFF", font="Arial 32", width=20, height=5)
    Label_Gametitle.pack()

    global Button_Play
    Button_Play = tk.Button(mainwindow, text="Start", width=10, height=2, command=startgame)
    global Button_Exit
    Button_Exit = tk.Button(mainwindow, text="Exit", width=10, height=2, command=exit)
    global Button_Help
    Button_Help = tk.Button(mainwindow, text="Help", width=10, height=2, command=help)
    global Button_LB  # leaderboard
    Button_LB = tk.Button(mainwindow, text="Leader Board", width=12, height=2, command=leaderboard.displayboard)

    Button_Play.place(x=700, y=350, anchor="center")
    Button_Exit.place(x=900, y=350, anchor="center")
    Button_Help.place(x=800, y=350, anchor="center")
    Button_LB.place(x=800, y=450, anchor="center")

    global Username
    Username = "anonymous"  # set default user name

    global Label_Nameinput
    Label_Nameinput = tk.Label(mainwindow, text="Your user name:", font="Arial 12")
    Label_Nameinput.place(x=720, y=280, anchor="e")
    global NameInput
    global NameInput_var
    NameInput_var = tk.StringVar()
    NameInput = tk.Entry(text="Please enter your username", textvariable=NameInput_var)
    NameInput.place(x=800, y=280, anchor="center")

    global Label_Author
    Label_Author = tk.Label(mainwindow, text="Developer: Ziyi Li", font="Arial 12", width=20, height=5)
    Label_Author.place(x=800, y=800, anchor="center")

    global GameCanvas
    GameCanvas = tk.Canvas(mainwindow, width=config.canvassize[0], height=config.canvassize[1], bg=config.bgcolor)

    mainwindow.focus_set()
    mainwindow.bind(f"<KeyPress-{config.bosskey}>", bosskey)


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
        distance += config.movespeed
        Trajectory.append(GameCanvas.coords(GameCharacter))
        if alive:
            if direction == "up":
                GameCanvas.create_line(GameCanvas.coords(GameCharacter), GameCanvas.coords(GameCharacter)[0],
                                       GameCanvas.coords(GameCharacter)[1] - config.movespeed)
                GameCanvas.move(GameCharacter, 0, -config.movespeed)
            elif direction == "left":
                GameCanvas.create_line(GameCanvas.coords(GameCharacter),
                                       GameCanvas.coords(GameCharacter)[0] - config.movespeed,
                                       GameCanvas.coords(GameCharacter)[1])
                GameCanvas.move(GameCharacter, -config.movespeed, 0)
            elif direction == "down":
                GameCanvas.create_line(GameCanvas.coords(GameCharacter), GameCanvas.coords(GameCharacter)[0],
                                       GameCanvas.coords(GameCharacter)[1] + config.movespeed)
                GameCanvas.move(GameCharacter, 0, config.movespeed)
            elif direction == "right":
                GameCanvas.create_line(GameCanvas.coords(GameCharacter),
                                       GameCanvas.coords(GameCharacter)[0] + config.movespeed,
                                       GameCanvas.coords(GameCharacter)[1])
                GameCanvas.move(GameCharacter, config.movespeed, 0)
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
        # print(event.char) # use for debug
        global point
        if event.char == config.keyup:
            Move("up")
        elif event.char == config.keyleft:
            Move("left")
        elif event.char == config.keydown:
            Move("down")
        elif event.char == config.keyright:
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
    Label_Author.place_forget()
    Label_Nameinput.place_forget()
    NameInput.place_forget()

    global point
    point = 0
    global distance
    distance = 0
    global alive
    alive = True

    global GameCanvas
    global Username
    global NameInput_var
    if NameInput_var.get() != "":
        Username = NameInput_var.get()

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
