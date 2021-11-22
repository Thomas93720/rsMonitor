
#! /usr/bin/python3

import os
#import obd
from sys import exit
from ctypes import c_long, pointer
import sdl2.ext
import sys
import sdl2
from sdl2 import *
from sdl2.sdlttf import *

vcurrentrpm = 0
voiltemp = 0
voilpressure = 0
vboostpressure = 0
vairflowtemp = 0
vexhausttemp = 0


def renderText(message, fontFile, color, fontSize):
    # Open the font
    global font, p2, surf
    SDL_ClearError()
    surf = None
    try:
        # assume python 3 and encode as byte
        font = TTF_OpenFont(str.encode(fontFile), fontSize)
    except:
        p3 = SDL_GetError()
        try:
            # python 2 import
            font = TTF_OpenFont(fontFile, fontSize)
        except:
            p2 = SDL_GetError()
        if font is None or not p2 == '' or not p3 == '':
            print("TTF_OpenFont error: ", p2, p3)
            return None

    try:
        surf = TTF_RenderText_Blended(font, str.encode(message), color)

    except:
        try:
            surf = TTF_RenderText_Blended(font, message, color)
        except:
            pass

    if surf is None:
        TTF_CloseFont(font)
        print("TTF_RenderText")
        return None

    TTF_CloseFont(font)
    return surf
    print("rendertext")


def drawframe(screen):
    global vcurrentrpm
    global voiltemp
    global voilpressure
    global vboostpressure
    global vairflowtemp
    global vexhausttemp

    myStr = str(voiltemp)
    for i in range(len(myStr)):
        surface.SDL_BlitSurface(digits[myStr[i]], None, screen, SDL_Rect(540 + (11 * i), 65))

    myStr = str(voilpressure)
    for i in range(len(myStr)):
        surface.SDL_BlitSurface(digits[myStr[i]], None, screen, SDL_Rect(540 + (11 * i), 175))

    myStr = str(vboostpressure)
    for i in range(len(myStr)):
        surface.SDL_BlitSurface(digits[myStr[i]], None, screen, SDL_Rect(540 + (11 * i), 285))

    myStr = str(vairflowtemp)
    for i in range(len(myStr)):
        surface.SDL_BlitSurface(digits[myStr[i]], None, screen, SDL_Rect(540 + (11 * i), 395))

    myStr = str(vcurrentrpm)
    for i in range(len(myStr)):
        surface.SDL_BlitSurface(digits[myStr[i]], None, screen, SDL_Rect(540 + (11 * i), 505))

    myStr = str(vexhausttemp)
    for i in range(len(myStr)):
        surface.SDL_BlitSurface(digits[myStr[i]], None, screen, SDL_Rect(540 + (11 * i), 615))

    # Valeurs oil etc
    surface.SDL_BlitSurface(OILTemp, None, screen, SDL_Rect(58, 62))
    surface.SDL_BlitSurface(OilPressure, None, screen, SDL_Rect(40, 172))
    surface.SDL_BlitSurface(BoostPressure, None, screen, SDL_Rect(20, 282))
    surface.SDL_BlitSurface(AirflowTemp, None, screen, SDL_Rect(35, 392))
    surface.SDL_BlitSurface(CurrentRPM, None, screen, SDL_Rect(35, 502))
    surface.SDL_BlitSurface(ExhaustTemp, None, screen, SDL_Rect(30, 612))
    # MAX
    surface.SDL_BlitSurface(max, None, screen, SDL_Rect(895, 105))
    surface.SDL_BlitSurface(max, None, screen, SDL_Rect(895, 215))
    surface.SDL_BlitSurface(max, None, screen, SDL_Rect(895, 325))
    surface.SDL_BlitSurface(max, None, screen, SDL_Rect(895, 435))
    surface.SDL_BlitSurface(max, None, screen, SDL_Rect(895, 545))
    surface.SDL_BlitSurface(max, None, screen, SDL_Rect(895, 655))


class Percent():

    def __init__(self, p1, p2, p3, p4, p5, p6):
        self.__p1 = p1
        self.__p2 = p2
        self.__p3 = p3
        self.__p4 = p4
        self.__p5 = p5
        self.__p6 = p6

    def changeValue(self, up, name, value):
        if (name == "p1"):
            if (up == False):
                self.set_p1(value - 1)
            else:
                self.set_p1(value + 1)
        if (name == "p2"):
            if (up == False):
                self.set_p2(value - 1)
            else:
                self.set_p2(value + 1)
        if (name == "p3"):
            if (up == False):
                self.set_p3(value - 1)
            else:
                self.set_p3(value + 1)
        if (name == "p4"):
            if (up == False):
                self.set_p4(value - 1)
            else:
                self.set_p4(value + 1)
        if (name == "p5"):
            if (up == False):
                self.set_p5(value - 1)
            else:
                self.set_p5(value + 1)
        if (name == "p6"):
            if (up == False):
                self.set_p6(value - 1)
            else:
                self.set_p6(value + 1)

    def get_p1(self):
        return self.__p1

    def set_p1(self, p1):
        if (p1 < 0):
            self.__p1 = 0
        elif (p1 > 100):
            self.__p1 = 100
        else:
            self.__p1 = p1

    def get_p2(self):
        return self.__p2

    def set_p2(self, p2):
        if (p2 < 0):
            self.__p2 = 0
        elif (p2 > 100):
            self.__p2 = 100
        else:
            self.__p2 = p2

    def get_p3(self):
        return self.__p3

    def set_p3(self, p3):
        if (p3 < 0):
            self.__p3 = 0
        elif (p3 > 100):
            self.__p3 = 100
        else:
            self.__p3 = p3

    def get_p4(self):
        return self.__p4

    def set_p4(self, p4):
        if (p4 < 0):
            self.__p4 = 0
        elif (p4 > 100):
            self.__p4 = 100
        else:
            self.__p4 = p4

    def get_p5(self):
        return self.__p5

    def set_p5(self, p5):
        if (p5 < 0):
            self.__p5 = 0
        elif (p5 > 100):
            self.__p5 = 100
        else:
            self.__p5 = p5

    def get_p6(self):
        return self.__p6

    def set_p6(self, p6):
        if (p6 < 0):
            self.__p6 = 0
        elif (p6 > 100):
            self.__p6 = 100
        else:
            self.__p6 = p6


def RGB_to_hex(RGB):
    RGB = [int(x) for x in RGB]
    return "#" + "".join(["0{0:x}".format(v) if v < 16 else
                          "{0:x}".format(v) for v in RGB])

def color_dict(gradient):
    return {"hex": [RGB_to_hex(RGB) for RGB in gradient],
            "r": [RGB[0] for RGB in gradient],
            "g": [RGB[1] for RGB in gradient],
            "b": [RGB[2] for RGB in gradient]}

def hex_to_RGB(hex):
    return [int(hex[i:i + 2], 16) for i in range(1, 6, 2)]

def linear_gradient(start_hex, finish_hex="#FF0000", n=780):
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    RGB_list = [s]
    for t in range(1, n):
        curr_vector = [
            int(s[j] + (float(t) / (n - 1)) * (f[j] - s[j]))
            for j in range(3)
        ]
        RGB_list.append(curr_vector)
    return color_dict(RGB_list)

class Gauge :
    def __init__(self, label, w, h, min, max,position,positionMax):
        self.__label = label
        self.__w = w
        self.__h = h
        self.__min = min
        self.__max = max
        self.__position = position
        self.__positionMax = positionMax
        self.__dirty = True

    def update(self):
        "redessine la gauge et passe dirty false"
        mGD = (linear_gradient(start_hex="#ffff00"))
        view = sdl2.ext.PixelView(screen)
        cpt = 0
        for k in range(self.__w):
            for j in range((self.__h)):
                view[self.__position + j][161 + k] = sdl2.ext.Color(mGD["r"][cpt], mGD["g"][cpt], mGD["b"][cpt])
            cpt += 1
        DrawTextForGauge(screen,self.__label,self.__position,self.__positionMax)
        self.__dirty = False

    def draw(self, x, y) :
        if self.__dirty == True :
            self.update()
        else :
            mGD = (linear_gradient(start_hex="#ffff00"))
            view = sdl2.ext.PixelView(screen)
            cpt = 0
            for k in range(self.__w) :
                for j in range((self.__h)):
                    view[x + j][y + k] = sdl2.ext.Color(mGD["r"][cpt], mGD["g"][cpt], mGD["b"][cpt])
                cpt += 1
            DrawTextForGauge(screen, self.__label, self.__position, self.__positionMax)

def DrawTextForGauge(screen,label,position,positionMax):

    myStr = str(label)
    for i in range(len(myStr)):
        surface.SDL_BlitSurface(digits[myStr[i]], None, screen, SDL_Rect(position))

    # Valeurs oil etc
    surface.SDL_BlitSurface(label, None, screen, SDL_Rect(position))
    # MAX
    surface.SDL_BlitSurface(max, None, screen, SDL_Rect(895, positionMax))


class Rect() :
    @staticmethod
    def DrawAllRectAndFill(surface, percentOne,percentTwo,percentThree,percentFour,percentFive,percentSix):
        positionFirst = 51
        positionSecond = 161
        positionThird = 271
        positionFourth = 381
        positionFifth = 491
        positionSixth = 601
        color = sdl2.ext.Color(255, 255, 255)
        x1, y1 = 160, 50
        x2, y2 = 940, 50
        x3, y3 = 160, 110
        x4, y4 = 940, 110
        nb = 6
        shift = 0
        for i in range(nb):
            sdl2.ext.line(surface, color, (x1, y1 + shift, x2, y2 + shift))
            sdl2.ext.line(surface, color, (x3, y3 + shift, x4, y4 + shift))
            sdl2.ext.line(surface, color, (x1, y1 + shift, x3, y3 + shift))
            sdl2.ext.line(surface, color, (x2, y2 + shift, x4, y4 + shift))
            shift += 110
        mGD = (linear_gradient(start_hex="#ffff00"))
        view = sdl2.ext.PixelView(screen)
        cpt = 0
        for k in range(int(780/100*percentOne)) :
            for j in range((60)):
                view[positionFirst + j][161 + k] = sdl2.ext.Color(mGD["r"][cpt], mGD["g"][cpt], mGD["b"][cpt])
            cpt += 1
        cpt = 0
        for k in range(int(780 / 100 * percentTwo)):
            for j in range((60)):
                view[positionSecond + j][161 + k] = sdl2.ext.Color(mGD["r"][cpt], mGD["g"][cpt], mGD["b"][cpt])
            cpt += 1
        cpt = 0
        for k in range(int(780 / 100 * percentThree)):
            for j in range((60)):
                view[positionThird + j][161 + k] = sdl2.ext.Color(mGD["r"][cpt], mGD["g"][cpt], mGD["b"][cpt])
            cpt += 1
        cpt = 0
        for k in range(int(780 / 100 * percentFour)):
            for j in range((60)):
                view[positionFourth + j][161 + k] = sdl2.ext.Color(mGD["r"][cpt], mGD["g"][cpt], mGD["b"][cpt])
            cpt += 1
        cpt = 0
        for k in range(int(780 / 100 * percentFive)):
            for j in range((60)):
                view[positionFifth + j][161 + k] = sdl2.ext.Color(mGD["r"][cpt], mGD["g"][cpt], mGD["b"][cpt])
            cpt += 1
        cpt = 0
        for k in range(int(780 / 100 * percentSix)):
            for j in range((60)):
                view[positionSixth + j][161 + k] = sdl2.ext.Color(mGD["r"][cpt], mGD["g"][cpt], mGD["b"][cpt])
            cpt += 1

def handleevent():
    eventH = SDL_Event()
    while SDL_PollEvent(eventH):
        if eventH.type == SDL_QUIT:
            return False
        elif eventH.type == SDL_WINDOWEVENT:
            if eventH.window.event == SDL_WINDOWEVENT_RESIZED:
                SDL_GetWindowSize(window, SCREEN_WIDTH, SCREEN_HEIGHT)
                x = SCREEN_WIDTH.contents.value / 2 - OILTemp.contents.w / 2
                y = SCREEN_HEIGHT.contents.value / 2 - OILTemp.contents.h / 2
    return True

def refreshValues(percent):
    global connection
    global vcurrentrpm
    global voiltemp
    global voilpressure
    global vboostpressure
    global vairflowtemp
    global vexhausttemp

    #rpm = connection.query(obd.commands.RPM, True)
    #if rpm.value is not None:
    #    vcurrentrpm = rpm.value.magnitude
    #    print("just read value  %f" % (vcurrentrpm))
    #else:
    #    print("couldn't read current value")
    voiltemp = 8
    voilpressure = 54
    vboostpressure = 5
    vairflowtemp = 47
    vexhausttemp = 14

    percent.set_p5(vcurrentrpm / 7000 * 100)

SDL_Init(SDL_INIT_VIDEO)
#connection = obd.OBD(fast=False, check_voltage=False)

try:
    window = SDL_CreateWindow(
        b"SDL2 TTF test",  # window title
        SDL_WINDOWPOS_CENTERED,  # initial x position
        SDL_WINDOWPOS_CENTERED,  # initial y position
        1024,  # width, in pixels
        768,  # height, in pixels
        SDL_WINDOW_RESIZABLE  # flags
    )
except:
    # used from another file because first didn't work
    window = SDL_CreateWindow(
        b'SDL2 TTF test 2',
        SDL_WINDOWPOS_UNDEFINED,
        SDL_WINDOWPOS_UNDEFINED,
        1024,
        768,
        SDL_WINDOW_SHOWN)

tfi = TTF_Init()
if tfi != 0:
    exit(1)

color = SDL_Color(255, 255, 255)

font = "Gadugi"
fontpath = font + ".ttf"

x = 0

OILTemp = renderText("OIL Temp", fontpath,color, 20)
OilPressure = renderText("Oil Pressure", fontpath,color, 20)
BoostPressure = renderText("Boost Pressure", fontpath,color, 20)
AirflowTemp = renderText("Airflow Temp", fontpath,color, 20)
CurrentRPM = renderText("Current RPM", fontpath,color, 20)
ExhaustTemp = renderText("Exhaust Temp", fontpath,color, 20)
max = renderText("max", fontpath,color, 15)

digits = dict()
digits["."] = renderText(".", fontpath,
                         color, 20)
for i in range(10):
    digits[str(i)] = renderText(str(i), fontpath,
                                color, 20)

if OILTemp is None:
    exit(1)

SCREEN_WIDTH = pointer(c_int(0))
SCREEN_HEIGHT = pointer(c_int(0))
SDL_GetWindowSize(window, SCREEN_WIDTH, SCREEN_HEIGHT)

x = SCREEN_WIDTH.contents.value / 2 - OILTemp.contents.w / 2
y = SCREEN_HEIGHT.contents.value / 2 - OILTemp.contents.h / 2
v = 200

screen = SDL_GetWindowSurface(window)

def run(screen):
    percent = Percent(p1=100, p2=75, p3=50, p4=25, p5=10, p6=5)

    startstamp = SDL_GetTicks()
    startvtimestamp = startstamp
    while True:
        now = SDL_GetTicks()

        if now - startstamp >= 1000:
            refreshValues(percent)
            startstamp = now

        r = handleevent()
        if r is False:
            break
        if now - startvtimestamp >= 1000:
            sdl2.ext.fill(screen, sdl2.ext.Color(0, 0, 0))
            Rect().DrawAllRectAndFill(screen, percent.get_p1(),percent.get_p2(),percent.get_p3(),percent.get_p4(),percent.get_p5(),percent.get_p6())
            drawframe(screen)
            SDL_UpdateWindowSurface(window)
            startvtimestamp = now
            print("redrawn screen")

run(screen)
SDL_DestroyWindow(window)
SDL_Quit()
