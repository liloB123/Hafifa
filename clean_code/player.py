from mutagen.easyid3 import EasyID3
import pygame
from tkinter.filedialog import *
from tkinter import *
from enum import Enum
pygame.init()

class ButtonAction(Enum):
        ADD_TO_LIST = "ADD TO LIST"
        PLAY_SONG = "PLAY SONG"
        PAUSE_UNPAUSE = "PAUSE/UNPAUSE"
        PREVIOUS_SONG = "PREVIOUS SONG"
        NEXT_SONG = "NEXT SONG" 

class SongPlayer:
    def __init__(self):
        self.list = list()
        self.pausing = False
        self.list_index = 0
        self.SONG_END = pygame.USEREVENT + 1
    
    def add(self):
        try:
            directory = askopenfilenames()
            for song_dir in directory:
                print(song_dir)
                self.list.append(song_dir)
            self.text.delete(0.0, END)

            for key, item in enumerate(self.list):
                song = EasyID3(item)
                song_data = (str(key + 1) + ' : ' + song['title'][0] + ' - '
                            + song['artist'][0])
                self.text.insert(END, song_data + '\n')
        except:
            pass
    
    def song_data(self):
        try:
            song = EasyID3(self.list[self.list_index])
            song_data = "Now playing: Nr:" + str(self.list_index + 1) + " " + \
                        str(song['title']) + " - " + str(song['artist'])
            return song_data
        except:
            pass

    def play(self):
        try:
            directory = self.list[self.list_index]
            pygame.mixer.music.load(directory)
            pygame.mixer.music.play(1, 0.0)
            pygame.mixer.music.set_endevent(self.SONG_END)
            self.pausing = False
            self.label['text'] = self.song_data()
        except:
            pass
    
    def pause_toggle(self):
        try:
            if self.pausing:
                pygame.mixer.music.unpause()
                self.pausing = False
            elif not self.pausing:
                pygame.mixer.music.pause()
                self.pausing = True
        except:
            pass

    def change_song(self, direction):
        try:
            self.list_index += direction
            
            if self.list_index >= len(self.list):
                self.list_index = 0
            elif self.list_index < 0:
                self.list_index = len(self.list) - 1

            self.play()
        except:
            pass
    
    def play_next(self):
        self.change_song(1)

    def play_previous(self):
        self.change_song(-1) 

class FrameApp(Frame):
    def __init__(self,master):
        super(FrameApp, self).__init__(master)
        self.grid()
        self.bg = 'AntiqueWhite1'
        self.width = 40
        self.label = Label(self, fg='Black',font=('Helvetica 12 bold italic',10),bg='ivory2')
        self.label.grid(row=6,column=0)
        self.text = Text(self,wrap=WORD,width=60)
        self.text.grid(row=8,column=0)

        self.song_player = SongPlayer()
        self.create_buttons()

    def add(self):
        self.song_player.add()

    def play(self):
        self.song_player.play()

    def pause_toggle(self):
        self.song_player.pause_toggle()

    def play_next(self):
        self.song_player.play_next()

    def play_previous(self):
        self.song_player.play_previous()
    
    def check_song(self):
        try:
            for event in pygame.event.get():
                if event.type == self.song_player.SONG_END:
                    self.play_next()
        except:
            pass
      
    def create_buttons(self):
        functions_array = [self.add, self.play, self.pause_toggle, self.play_previous, self.play_next]
        
        for index, action in enumerate(ButtonAction):
            button = Button(self, 
                            text=action.value, 
                            command=functions_array[index],
                            bg=self.bg, 
                            width=self.width)
            button.grid(row=index+1, column=0)

window = Tk()
window.geometry("500x500")
window.title("MP3 Music Player")
app = FrameApp(window)

while True:
    app.check_song()
    app.update()