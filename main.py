#! /usr/bin/python3

import os
import obd
from sys import exit
from ctypes import c_long, pointer
import sdl2.ext
import sys
import sdl2
from sdl2 import *
from sdl2.sdlttf import *
import random
from collections import defaultdict

vcurrentrpm = 0
voiltemp = 0
voilpressure = 0
vFuelLevel = 13
vEngineLoad = 0
vThrottlePos = 0

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
    global vSpeed
    global vcoolantTemp
    global vFuelLevel
    global vMaf
    global vcoolantTemp

    # Valeurs oil etc
    surface.SDL_BlitSurface(OILTemp, None, screen, SDL_Rect(58, 62))
    surface.SDL_BlitSurface(OilPressure, None, screen, SDL_Rect(40, 172))
    surface.SDL_BlitSurface(FuelLevel, None, screen, SDL_Rect(20, 282))
    surface.SDL_BlitSurface(EngineLoad, None, screen, SDL_Rect(35, 392))
    surface.SDL_BlitSurface(CurrentRPM, None, screen, SDL_Rect(35, 502))
    surface.SDL_BlitSurface(ThrottlePos, None, screen, SDL_Rect(30, 612))
    # MAX
    surface.SDL_BlitSurface(max, None, screen, SDL_Rect(895, 105))
    surface.SDL_BlitSurface(max, None, screen, SDL_Rect(895, 215))
    surface.SDL_BlitSurface(max, None, screen, SDL_Rect(895, 325))
    surface.SDL_BlitSurface(max, None, screen, SDL_Rect(895, 435))
    surface.SDL_BlitSurface(max, None, screen, SDL_Rect(895, 545))
    surface.SDL_BlitSurface(max, None, screen, SDL_Rect(895, 655))

def drawNumber(screen) :
    global vcurrentrpm
    global voiltemp
    global voilpressure
    global vFuelLevel
    global vEngineLoad
    global vThrottlePos
    value = 65
    for n in range(6):
        surface.SDL_FillRect(screen, SDL_Rect(945, value, 54, 35), 0xFF000000)
        value += 110
    myStr = str(int(voiltemp))
    for i in range(len(myStr)):
        surface.SDL_BlitSurface(digits[myStr[i]], None, screen, SDL_Rect(945 + (11 * i), 65))
    myStr = str(int(voilpressure / 100))
    for i in range(len(myStr)):
        surface.SDL_BlitSurface(digits[myStr[i]], None, screen, SDL_Rect(945 + (11 * i), 175))
    myStr = str(int(vFuelLevel))
    for i in range(len(myStr)):
        surface.SDL_BlitSurface(digits[myStr[i]], None, screen, SDL_Rect(945 + (11 * i), 285))
    myStr = str(int(vEngineLoad))
    for i in range(len(myStr)):
        surface.SDL_BlitSurface(digits[myStr[i]], None, screen, SDL_Rect(945 + (11 * i), 395))
    myStr = str(int(vcurrentrpm))
    for i in range(len(myStr)):
        surface.SDL_BlitSurface(digits[myStr[i]], None, screen, SDL_Rect(945 + (11 * i), 505))
    myStr = str(int(vThrottlePos * 100))
    for i in range(len(myStr)):
        surface.SDL_BlitSurface(digits[myStr[i]], None, screen, SDL_Rect(945 + (11 * i), 615))

def drawWhiteSquare() :
    view = sdl2.ext.PixelView(screen)
    cpt = 0
    base = 51
    end = 160
    for n in range(2):
        for k in range(6):
            for j in range((60)):
                view[base + cpt][end] = sdl2.ext.Color(255, 255, 255)
                cpt += 1
            cpt = 0
            base += 110
        cpt = 0
        base = 51
        end = 940
    index = 50
    for i in range(6):
        for k in range(781):
            view[index][160 + k] = sdl2.ext.Color(255, 255, 255)
        index += 110

    index = 111

    for i in range(6):
        for k in range(781):
            view[index][160 + k] = sdl2.ext.Color(255, 255, 255)
        index += 110

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

def covertRGBToTuple() :
    toConvert = linear_gradient(start_hex="#ffff00")
    myDictRGB = defaultdict(list)
    for i in range(780):
        myDictRGB[i] = (toConvert["r"][i],toConvert["g"][i],toConvert["b"][i])
    return myDictRGB

mGD = covertRGBToTuple()

class Gauge :
    def __init__(self, w, h, min, max,position,positionMax):
        self.__w = w
        self.__h = h
        self.__min = min
        self.__max = max
        self.__position = position
        self.__positionMax = positionMax
        self.__dirty = True

    def update(self):
        "redessine la gauge et passe dirty false"
        view = sdl2.ext.PixelView(screen)
        cpt = 0
        surface.SDL_FillRect(screen, SDL_Rect(161, self.__position, 779, 60), 0xFF000000)
        for k in range(self.__w):
            for j in range((self.__h)):
                r, g, b = mGD[cpt]
                view[self.__position + j][self.__positionMax + k] = sdl2.ext.Color(r, g, b)
            cpt += 1
        self.__dirty = False

    def draw(self, x, y) :
        self.__position = x
        self.__positionMax = y
        if self.__dirty == True :
            self.update()
            print("DirtyTrue")
        else :
            print("DirtyFalse")

    def getDirty(self):
        return self.__dirty

    def setDirtyTrue(self):
        self.__dirty = True

    def setWidth(self,w):
        self.__w = w

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

def refreshValues():
    global connection
    global vcurrentrpm
    global voiltemp
    global voilpressure
    global vFuelLevel
    global vEngineLoad
    global vThrottlePos

    rpm = connection.query(obd.commands.RPM, True)
    if rpm.value is not None:
        if(vcurrentrpm != rpm.value.magnitude):
            vcurrentrpm = rpm.value.magnitude
            myJauge.setWidth(int(vcurrentrpm*780/7000))
            myJauge.setDirtyTrue()
        print("just read value  %f" % (vcurrentrpm))
    else:
        print("couldn't read current value")
    oiltemp = connection.query(obd.commands.OIL_TEMP, True)
    if oiltemp.value is not None:
        if (voiltemp != oiltemp.value.magnitude):
            voiltemp = oiltemp.value.magnitude
            myJauge2.setWidth(int(voiltemp*780/150))
            myJauge2.setDirtyTrue()
        print("just read value  %f" % (voiltemp))
    else:
        print("couldn't read current value")
    oilpressure = connection.query(obd.commands.FUEL_RAIL_PRESSURE_ABS, True)
    if oilpressure.value is not None:
        if (voilpressure != oilpressure.value.magnitude):
            voilpressure = oilpressure.value.magnitude
            myJauge3.setWidth(int(voilpressure * 780 / 80000))
            myJauge3.setDirtyTrue()
        print("just read value  %f" % (voilpressure))
    else:
        print("couldn't read current value")
    FuelLevel = connection.query(obd.commands.FUEL_LEVEL, True)
    if FuelLevel.value is not None:
        if (vFuelLevel != int(13)):
            vFuelLevel = FuelLevel.value.magnitude
            myJauge4.setWidth(int(vFuelLevel * 780 / 60))
            myJauge4.setDirtyTrue()
        print("just read value  %f" % (vFuelLevel))
    else:
        print("couldn't read current value")
    EngineLoad = connection.query(obd.commands.ENGINE_LOAD, True)
    if EngineLoad.value is not None:
        if (vEngineLoad != EngineLoad.value.magnitude):
            vEngineLoad = EngineLoad.value.magnitude
            myJauge5.setWidth(int(vEngineLoad * 780 / 100))
            myJauge5.setDirtyTrue()
        print("just read value  %f" % (vEngineLoad))
    else:
        print("couldn't read current value")
    ThrottlePos = connection.query(obd.commands.THROTTLE_POS, True)
    if ThrottlePos.value is not None:
        if (vThrottlePos != ThrottlePos.value.magnitude):
            vThrottlePos = ThrottlePos.value.magnitude
            myJauge6.setWidth(int(vThrottlePos*780/100))
            myJauge6.setDirtyTrue()
        print("just read value  %f" % (vThrottlePos))
    else:
        print("couldn't read current value")

SDL_Init(SDL_INIT_VIDEO)
connection = obd.OBD(portstr="/dev/ttyUSB0",fast=False, check_voltage=False)

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
FuelLevel = renderText("Fuel Level", fontpath,color, 20)
EngineLoad = renderText("Engine Load", fontpath,color, 20)
CurrentRPM = renderText("Current RPM", fontpath,color, 20)
ThrottlePos = renderText("Throttle Position", fontpath,color, 20)
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

view = sdl2.ext.PixelView(screen)
view[50][20] = sdl2.ext.Color(0, 255, 0)
drawWhiteSquare()
drawframe(screen)
w, h, min, max, position, positionMax = 0, 60, 200, 300, 51, 161
myJauge = Gauge(w, h, min, max, position, positionMax)
myJauge2 = Gauge(w, h, min, max, position, positionMax)
myJauge3 = Gauge(w, h, min, max, position, positionMax)
myJauge4 = Gauge(w, h, min, max, position, positionMax)
myJauge5 = Gauge(w, h, min, max, position, positionMax)
myJauge6 = Gauge(w, h, min, max, position, positionMax)

def run(screen):
    startstamp = SDL_GetTicks()
    startvtimestamp = startstamp
    while True:
        global vcurrentrpm
        global vSpeed
        global vcoolantTemp
        global vFuelLevel
        global vMaf
        global vcoolantTemp
        now = SDL_GetTicks()
        if now - startstamp >= 1:
            refreshValues()
            startstamp = now
        r = handleevent()
        if r is False:
            break
        if now - startvtimestamp >= 1:
            SDL_UpdateWindowSurface(window)
            drawNumber(screen)
            if(myJauge.getDirty()):
                myJauge.draw(51, 161)
            if (myJauge2.getDirty()):
                myJauge2.draw(161, 161)
            if (myJauge3.getDirty()):
                myJauge3.draw(271, 161)
            if (myJauge4.getDirty()):
                myJauge4.draw(381, 161)
            if (myJauge5.getDirty()):
                myJauge5.draw(491, 161)
            if (myJauge6.getDirty()):
                myJauge6.draw(601, 161)
            startvtimestamp = now
            print("redrawn screen")
run(screen)
SDL_DestroyWindow(window)
SDL_Quit()