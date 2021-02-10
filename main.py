import logging
import os
import nathlib as nlib

version_name = "snapshot_001"
version_number = 1

os.remove('latest.log')
nlib.start_logs("latest.log")
nlib.log("Launching game version {0} ...".format(version_name), "info")
# Importation des modules

# try:
print("------------------------------Pygame--Details--------------------------")
import pygame

print("-----------------------------------------------------------------------")
import sys
import webbrowser
import time
import random
import pickle
import math
import tkinter as tk
import tkinter.ttk as ttk
from pygame import gfxdraw
import threading

# except ImportError:
# print("[ERROR]: Failed to import modules !")
# from sys import exit

# exit()


try:
    from scripts.util.FileManager import *

    for x in range(0, lang_number):
        exec("from scripts.util.FileManager import " + lang_files_to_load[x])
except:
    nlib.log("Failed to load resources, aborting ...", "critical")
    sys.exit()

# Initialisation de Pygame

pygame.init()
pygame.font.init()
pygame.mixer.init()  # Sons de pygame.

# Definition de la fenetre

window_x = 1280
window_y = 720
screen = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption("Space Escape")
clock = pygame.time.Clock()
FPS = 60
# ressources à charger

img_spaceship = pygame.image.load("resources/resource_0").convert_alpha()
img_star = pygame.image.load("resources/resource_1").convert()
img_icon_spaceship = pygame.image.load("resources/resource_2").convert_alpha()
img_background = pygame.image.load("resources/resource_3").convert()
img_logo = pygame.image.load("resources/resource_4").convert_alpha()
img_btn_normal = pygame.image.load("resources/resource_5").convert()
img_btn_hovered = pygame.image.load("resources/resource_6").convert()
btn_font = pygame.font.SysFont('Comic Sans MS', 30)

correction_angle = 90

pygame.display.set_icon(img_icon_spaceship)

spritegroup = pygame.sprite.Group()

isMenu = True

# fichier lang

lang = lang_files_names[settings_list[0]]
default_lang = eval(lang)

play_btn_text = btn_font.render(default_lang[0], False, (0, 0, 255))
settings_btn_text = btn_font.render(default_lang[1], False, (0, 0, 255))


# definition du joueur

class Var:
    def __init__(self):
        super(Var, self).__init__()
        self.is_settings_to_save = False
        self.is_update_checked = False

    def set_value(self, var_name, var_value):
        if var_name == "is_settings_to_save":
            self.is_settings_to_save = var_value
        if var_name == "is_update_checked":
            self.is_update_checked = var_value

    def get_value(self, var_name):
        return eval("self." + var_name)


global_var = Var()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_spaceship
        self.rect = self.image.get_rect()  # Adapte le taille du personnage a la taille de l'image.
        self.velocity = [0, 0]
        self.rect.x = window_x / 2.15
        self.rect.y = window_y / 2.15


class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_star
        self.rect = self.image.get_rect()  # Adapte le taille du personnage a la taille de l'image.
        self.velocity = [0, 0]
        self.rect.x = random.randint(0, window_x)
        self.rect.y = random.randint(0, window_y)


class Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_btn_normal
        self.rect = self.image.get_rect()  # Adapte le taille du personnage a la taille de l'image.
        self.velocity = [0, 0]
        self.rect.x = window_x / 2.5
        self.rect.y = window_y / 2
        self.isHovered = False
        self.isClicked = False
        self.isMenu = True
        self.maxX = 728
        self.minX = 512
        self.minY = 362
        self.maxY = 417
        self.type = 'play'

    def update(self, isMenu):
        if self.maxX > mouse[0] > self.minX and self.minY < mouse[1] < self.maxY:
            self.isHovered = True
        else:
            self.isHovered = False
        if self.isClicked:
            if self.type == 'play':
                self.isMenu = False
                self.isClicked = False
            elif self.type == 'settings':
                open_settings()
                self.isClicked = False


def open_settings():
    global_var.set_value("is_update_checked", False)

    def check_update_main():
        update_result = nlib.get_json_from_url("https://raw.githubusercontent.com/SiniKraft/"
                                               "Space-Escape/master/update.json")

        def download():
            webbrowser.open(update_result["version"]["latest"]["download"])

        if update_result["version"]["latest"]["number"] > version_number:
            txt_to_config = "Version : {0}, Latest : {1}".format(version_name,
                                                                 update_result["version"]["latest"]["name"])
            btn_update2 = ttk.Button(settings_window, text="Download", command=download)
            btn_update2.place(x=40, y=145)
        else:
            txt_to_config = "Version : {0}, You are up to date".format(version_name)
        update_txt.config(text=txt_to_config)

    def save_window_settings():
        global_var.set_value("is_settings_to_save", True)
        settings_window.destroy()

    global_var.set_value("is_settings_to_save", False)
    settings_window = tk.Tk()
    settings_window.title(default_lang[1])
    # move window center
    winWidth = settings_window.winfo_reqwidth()
    winwHeight = settings_window.winfo_reqheight()
    posRight = int(settings_window.winfo_screenwidth() / 2 - winWidth / 2)
    posDown = int(settings_window.winfo_screenheight() / 2 - winwHeight / 2)
    settings_window.geometry("+{}+{}".format(posRight, posDown))
    settings_window.configure(width=500, height=400)
    settings_window.resizable(0, 0)
    variable = tk.StringVar(settings_window)
    variable.set(settings_list[0])
    img = tk.PhotoImage(file="resources/resource_7")
    panel = tk.Label(settings_window, image=img)
    text = ttk.Label(settings_window, text=default_lang[3])
    text.place(x=170, y=50)
    update_txt = ttk.Label(settings_window, text="Version : {0}".format(version_name))
    update_txt.place(x=170, y=125)
    btn_update = ttk.Button(settings_window, text="Check for updates", command=check_update_main)
    btn_update.place(x=40, y=125)
    w = ttk.OptionMenu(settings_window, variable, settings_list[0], *lang_list)
    w.place(x=250, y=50)
    btn = ttk.Button(settings_window, text=default_lang[4], command=save_window_settings)
    btn.place(x=215, y=365)
    panel.pack()
    settings_window.mainloop()
    if global_var.get_value("is_settings_to_save"):
        settings_list[0] = variable.get()
        nlib.save(settings_list, "settings.ini")


play_btn = Button()
settings_btn = Button()
settings_btn.maxX = 728
settings_btn.maxY = 492
settings_btn.minX = 512
settings_btn.minY = 436
settings_btn.type = 'settings'

star = Star()
player = Player()
# Definition de la fenetre
continuer = True
playBtnIsClicked = False
inSpace = False
while continuer:
    if play_btn.isClicked:
        pass
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        if event.type == pygame.K_DOWN:
            if event.key == pygame.K_ESCAPE:
                continuer = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 728 > mouse[0] > 512 and 362 < mouse[1] < 417:  # check if btn is clicked.
                play_btn.isClicked = True
            if 728 > mouse[0] > 512 and 436 < mouse[1] < 492:
                settings_btn.isClicked = True

    mx, my = pygame.mouse.get_pos()
    dx, dy = mx - player.rect.centerx, my - player.rect.centery
    angle = math.degrees(math.atan2(-dy, dx)) - correction_angle

    rot_image = pygame.transform.rotate(player.image, angle)
    rot_image_rect = rot_image.get_rect(center=player.rect.center)
    screen.blit(img_background, (0, 0))
    if play_btn.isMenu:
        play_btn.update(isMenu)
        # pygame.gfxdraw.pixel(surface, 11, 11, 'YELLOW')
        settings_btn.update(isMenu)
        screen.blit(img_logo, (window_x / 5.2, window_y / 6))
        if play_btn.isHovered:  # check if btn play is hovered
            screen.blit(img_btn_hovered, (window_x / 2.5, window_y / 2))
        else:
            screen.blit(img_btn_normal, (window_x / 2.5, window_y / 2))
        screen.blit(play_btn_text, (window_x / 2.2, window_y / 1.97))
        if settings_btn.isHovered:  # check if btn settings is hovered
            screen.blit(img_btn_hovered, (window_x / 2.5, window_y / 1.65))
        else:
            screen.blit(img_btn_normal, (window_x / 2.5, window_y / 1.65))
        screen.blit(settings_btn_text, (window_x / 2.35, window_y / 1.637))
    else:
        if inSpace:
            screen.blit(img_background, (0, 0))
            screen.blit(rot_image, rot_image_rect.topleft)
    pygame.display.update()
pygame.quit()
nlib.log("Game stopped !", "info")
