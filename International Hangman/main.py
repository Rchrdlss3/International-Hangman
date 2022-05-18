from tkinter import*
from tkinter import Tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font
import mysql.connector
import random
import pandas as pd
from PIL import ImageTk, Image  
import googletrans
from googletrans import Translator

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="ZTIwpEp646939",
    database="UserInfos"
    )

cursor = db.cursor()
translator = Translator()
'''
This takes every word from the csv file and stores them in each list depending on the length of the word
'''
levelOneWords = []
levelTwoWords = []
levelThreeWords = []
levelFourWords = []
levelFiveWords = []
df = pd.read_csv('words.csv')

words = df['words']
imgai = 1

for word in words:
    if len(word) <= 5:
        levelOneWords.append(word)
        
for word in words:
    if len(word) == 6:
        levelTwoWords.append(word)
        
for word in words:
    if len(word) == 7:
        levelThreeWords.append(word)
        
for word in words:
    if len(word) == 8:
        levelFourWords.append(word)
        
for word in words:
    if len(word) > 8:
        levelFiveWords.append(word)


class Window1:
    def __init__(self,master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("400x200")
        self.master.resizable(False,False)
        self.master.config(bg='lavender')
        self.frame = Frame(self.master, bg = "lavender")
        self.frame.pack()
        
        global username
        global password
        username = tkinter.StringVar()
        password = tkinter.StringVar()
        
        self.labelUser = tkinter.Label(self.master, text="Username: ",background ="lavender",foreground ="white",font="Arial 8 bold")
        self.labelUser.place(x=25,y=25)
        self.entryUser = tkinter.Entry(self.master,textvariable = username)
        self.entryUser.place(x=100,y=25)
        
        self.labelPass = tkinter.Label(self.master,text="Password: ", background ="lavender",foreground ="white",font = "Arial 8 bold")
        self.labelPass.place(x=25,y=50) 
        self.entryPass = tkinter.Entry(self.master,textvariable = password)
        self.entryPass.place(x=100,y=50)
        self.buttonLogin = tkinter.Button(self.master,text="Login",font="Arial 8 bold",command = self.logs)
        self.buttonLogin.place(height = 45, width = 60,x= 100,y=75)
        
        self.buttonRegister = tkinter.Button(self.master,text="Register",font="Arial 8 bold",command = register)
        self.buttonRegister.place(height = 45, width = 60,x=160,y=75)
        
    def logs(self):
        sql = "SELECT * FROM userinfo WHERE BINARY username = '%s' AND BINARY userpassw = '%s'" %(username.get(),password.get())
        cursor.execute(sql)
        global logresult
        logresult = cursor.fetchone()
        if logresult:
            global u
            u = User(logresult[1],logresult[2],logresult[3])
            self.new_window()
        
        else:
            tkinter.messagebox.showwarning(message="Invalid credentials. Username or Password is invalid")
            
    def new_window(self):
        self.newWindow = Toplevel(self.master)
        self.app = Window2(self.newWindow)
        
#Second window class is the game class.       
class Window2:
    global u
    def __init__(self,master):
        self.master = master
        self.master.title("Hangman Game")
        self.master.geometry("800x500")
        self.master.config(bg='cadet blue')
        hangFrame = tkinter.Frame(self.master,width=200,height=500,bg='red',borderwidth=0)
        hangFrame.grid(row=0,column=0)
        
        self.wordFrame = tkinter.Frame(self.master,borderwidth=0,bg = 'cadet blue') 
        self.wordFrame.grid(row=0,column=1,rowspan=2)
        
        self.levelFrame = tkinter.Frame(self.master,bg='cadet blue',width=200,height=600)
        self.levelFrame.grid(row=0,column=3)
        
        self.transFrame = tkinter.Frame(self.master,bg='cadet blue',width=200,height=600)
        self.transFrame.grid(row=0,column=4)
        
        self.chalkFont = tkinter.font.Font(family ="chalkfont",size= 30)
        
        ####Normale photos
        self.levelonephoto = tkinter.PhotoImage(file= "buttons/levelone.png")
        self.leveltwophoto = tkinter.PhotoImage(file= "buttons/leveltwo.png")
        self.levelthreephoto = tkinter.PhotoImage(file= "buttons/levelthree.png")
        self.levelfourphoto = tkinter.PhotoImage(file= "buttons/levelfour.png")
        self.levelfivephoto = tkinter.PhotoImage(file= "buttons/levelfive.png")
        ####DISABLED PHOTOS
        self.levelonephotoDISABLED = tkinter.PhotoImage(file="buttons/leveloned.png")
        self.leveltwophotoDISABLED = tkinter.PhotoImage(file= "buttons/leveltwod.png")
        self.levelthreephotoDISABLED = tkinter.PhotoImage(file= "buttons/levelthreed.png")
        self.levelfourphotoDISABLED = tkinter.PhotoImage(file= "buttons/levelfourd.png")
        self.levelfivephotoDISABLED = tkinter.PhotoImage(file= "buttons/levelfived.png")
        
        #BUTTONS FOR LEVEL FRAME, TO CHOOSE THE LEVELS
        if u.highestlvl >=1:
            self.lvloneBtn = tkinter.Button(self.levelFrame,text='Level One',bg='#629ea0',highlightbackground='#629ea0',command=self.levelOneWord,image=self.levelonephoto)
        else:
            self.lvloneBtn = tkinter.Button(self.levelFrame,text='Level One',state= DISABLED,fg='cadet blue',highlightbackground='cadet blue',command= self.levelOneWord,image=self.levelonephotoDISABLED)
        self.lvloneBtn.grid()
        if u.highestlvl >=2:
            self.lvltwoBtn = tkinter.Button(self.levelFrame,text='Level Two',bg='cadet blue',highlightbackground='cadet blue',command=self.levelTwoWord,image=self.leveltwophoto)
        else:
            self.lvltwoBtn = tkinter.Button(self.levelFrame,text='Level Two',state= DISABLED,bg='cadet blue',highlightbackground='cadet blue',command=self.levelTwoWord,image=self.leveltwophotoDISABLED)
        self.lvltwoBtn.grid()
        
        if u.highestlvl >=3:
            self.lvlthreeBtn = tkinter.Button(self.levelFrame,text='Level Three',bg='cadet blue',highlightbackground='cadet blue',command=self.levelThreeWord,image= self.levelthreephoto)
        else:
            self.lvlthreeBtn = tkinter.Button(self.levelFrame,text='Level Three',state= DISABLED,bg='cadet blue',highlightbackground='cadet blue',command=self.levelThreeWord,image= self.levelthreephotoDISABLED)
        self.lvlthreeBtn.grid()
        
        if u.highestlvl >=4:
            self.lvlfourBtn = tkinter.Button(self.levelFrame,text='Level Four',bg='cadet blue',highlightbackground='cadet blue',command=self.levelFourWord, image= self.levelfourphoto)
        else:
            self.lvlfourBtn = tkinter.Button(self.levelFrame,text='Level Four',state= DISABLED,bg='cadet blue',highlightbackground='cadet blue',command=self.levelFourWord, image= self.levelfourphotoDISABLED)
        self.lvlfourBtn.grid()
        
        if u.highestlvl ==5:
            self.lvlfiveBtn = tkinter.Button(self.levelFrame,text='Level Five',bg='cadet blue',highlightbackground='cadet blue',command=self.levelFiveWord, image= self.levelfivephoto)
        else:
            self.lvlfiveBtn = tkinter.Button(self.levelFrame,text='Level Five',state= DISABLED,bg='cadet blue',highlightbackground='cadet blue',command=self.levelFiveWord, image= self.levelfivephotoDISABLED)
        self.lvlfiveBtn.grid()
        
        
        ##TRANSLATION
        self.languages = googletrans.LANGUAGES 
        self.language_list = list(self.languages.values())
        self.changeBtn = tkinter.Button(self.transFrame,text='Change Language',bg='cadet blue',highlightbackground='cadet blue',command= self.translateGame)
        self.changeBtn.grid(row=0,column=0)
        self.trans_combo = ttk.Combobox(self.transFrame,width=15,value=self.language_list)
        self.trans_combo.current(21)
        self.trans_combo.grid(row=1,column=0)

        self.photo = tkinter.PhotoImage(file= "hangpics/00.png")
        self.label1 = tkinter.Label(hangFrame, image= self.photo,borderwidth=0,highlightthickness=0)
        self.label1.photo = self.photo
        self.label1.grid()        
        
        self.userEntry = tkinter.Entry(self.wordFrame,bg = 'cadet blue',width =12,font= self.chalkFont)
        self.userEntry.grid(row=1,column=0)
        self.userEntry.bind('<Return>',self.validateEntry)
        
        global ai 
        ai = 0
        
    def translateGame(self):
        for key, value in self.languages.items():
            if (value == self.trans_combo.get()):
                transkey = key
        translatedword = translator.translate(self.randomword, dest= str(transkey))
        self.randomword = translatedword.text
        self.randomWord()
    
    def chooseLevel(self):
        self.randomWord()
        
    def validateEntry(self,e):
        global logresult
        global u
        self.temp = list(self.censoredstr)
        if len(self.userEntry.get()) > 1:
            messagebox.showerror('ERROR', "Sorry, you're only limited to one character")
            self.userEntry.delete(0,END)
        else:
            pass
        
        if self.userEntry.get() in self.wordmap.values():
            ch = self.userEntry.get()
            for i in range(len(self.randomword)):
                if self.randomword[i] == ch:
                    self.temp[i] = ch
                    self.censoredstr = "".join(self.temp)
            self.censoredlbl.config(text=self.censoredstr)
        else:
            self.addimg()
        self.userEntry.delete(0,END)
        if self.censoredlbl.cget("text") == self.randomword:
            self.censoredlbl.config(text=self.randomword)
            self.censoredlbl.update()
            self.gameWon()
    
    def gameWon(self):
        global imgai
        imgai = 0
        tkinter.messagebox.showinfo("Game won", "Congrats! You've won. The word was: %s"%(self.censoredlbl.cget("text")))
        u.highestlvl = 1
        if self.randomword in levelOneWords:
            u.highestlvl = 2
        elif self.randomword in levelTwoWords:
            u.highestlvl = 3
        elif self.randomword in levelThreeWords:
            u.highestlvl = 4
        elif self.randomword in levelFourWords:
            u.highestlvl = 5
        sql = "UPDATE userInfo SET highestlevel = %s WHERE userid = %s"%(u.highestlvl,logresult[0])
        cursor.execute(sql)
        db.commit()
        self.censoredstr = ''
        self.censoredlbl.config(text=self.censoredstr)
        self.photo = tkinter.PhotoImage(file= "hangpics/00.png")
        self.label1.config(image=self.photo)      
        if u.highestlvl >=2:
            self.lvltwoBtn.config(image= self.leveltwophoto)
            self.lvltwoBtn["state"] = NORMAL
            self.lvltwoBtn.update()
        if u.highestlvl >=3:
            self.lvlthreeBtn.config(image= self.levelthreephoto)
            self.lvlthreeBtn["state"] = NORMAL
            self.lvlthreeBtn.update()
        if u.highestlvl >=4:
            self.lvlfourBtn.config(image = self.levelfourphoto)
            self.lvlfourBtn["state"] = NORMAL
            self.lvlfourBtn.update()
        if u.highestlvl ==5:
            self.lvlfiveBtn.config(image= self.levelfivephoto)
            self.lvlfiveBtn["state"] = NORMAL
            self.lvlfiveBtn.update()
        
    def gameOver(self):
        global imgai
        tkinter.messagebox.showinfo('Game over','You have reached the total amount of tries.')
        imgai = 0
        self.censoredstr = ''
        self.censoredlbl.config(text=self.censoredstr)
        self.photo = tkinter.PhotoImage(file= "hangpics/00.png")
        self.label1.config(image=self.photo)
        self.randomWord()
        
    def addimg(self):
        global imgai
        if imgai == 10:
            self.gameOver()
        else:
            self.photo = tkinter.PhotoImage(file= "hangpics/0" +str(imgai)+".png")
            self.label1.config(image=self.photo)
        imgai+=1
        
    def levelOneWord(self):
        self.randomword = levelOneWords[random.randrange(len(levelOneWords)-1)]
        self.randomWord()
        
    def levelTwoWord(self):
        self.randomword = levelTwoWords[random.randrange(len(levelTwoWords)-1)]
        self.randomWord()
        
    def levelThreeWord(self):
        self.randomword = levelThreeWords[random.randrange(len(levelThreeWords)-1)]
        self.randomWord()
        
    def levelFourWord(self):
        self.randomword = levelFourWords[random.randrange(len(levelFourWords)-1)]
        self.randomWord()
    def levelFiveWord(self):
        self.randomword = levelFiveWords[random.randrange(len(levelFiveWords)-1)]
        self.randomWord()
        
    def randomWord(self):
        self.wordmap = {}
        self.censoredstr = ''
        self.censoredlbl = tkinter.Label(self.wordFrame,text= self.censoredstr, bg='cadet blue',foreground ="white",font=self.chalkFont)
        self.censoredlbl.grid(row=0,column=0,columnspan= 2)
        keyincrement = 0
        for ch in self.randomword:
            if ch in self.wordmap.keys():
                self.wordmap[ch +str(keyincrement)] = ch
                keyincrement +=1
            else:
                self.wordmap[ch] = ch
            self.censoredstr = self.censoredstr + '_'
        self.censoredlbl.config(text=self.censoredstr)
        print(self.wordmap)
        
class User():
    def __init__(self,username,password,highestlvl):
        self.username = username
        self.password = password
        self.highestlvl = highestlvl

    def changePassword():
        pass
    def resetLevel():
        pass
    
    def createuser(self):
        x = input("Enter username: ")
        y = input("Enter Password")
        yverify = input("Verify Password: ")
        if y == yverify:
            pass
        else:
            print("Passwords do not match. Please re-enter.")
            y = input("Enter Password")
            yverify = input("Verify Password: ")
        cursor.execute()
        cursor.execute("INSERT INTO userInfo (``,``) VALUES (%s,%s)")%(x,y)
        

def fillusers():
    for x in cursor.fetchall():
        pass 

def register():
    sql = "INSERT INTO userInfo (username,userpassw) VALUES(%s,%s)"
    val = (username.get(),password.get())
    cursor.execute(sql,val)
    db.commit()



def main():
    root = Tk()
    app = Window1(root)
    root.mainloop()

if __name__ == '__main__':
    main()
