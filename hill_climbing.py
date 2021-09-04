import subprocess
import sys
import time
from datetime import datetime
#import threading
import os
from PIL import Image

continue_button = (1658, 780)
start = (1690, 700)
gas = (2050, 850)
brake = (380, 850)
pause = (2151, 55)
restart = (1218, 534)
twitter = (710, 733)

def threadclick(xy, t=300):
    x, y = xy
    #return subprocess.run(["adb", "shell",  "input", "tap", f"{x}", f"{y}"])
    threading.Thread(
        target=subprocess.run,
        args=(["adb", "shell", "input", "swipe", f"{x}", f"{y}", f"{x}", f"{y}", f"{t}"],),
    )

def click(xy, t=300):
    x, y = xy
    subprocess.run(["adb", "shell", "input", "swipe", f"{x}", f"{y}", f"{x}", f"{y}", f"{t}"])

def redo():
    click(pause)
    click(restart)

def continuestart():
    while getstatus() != "start":
        click(continue_button)
    click(start)

def adamspeed(n=100, t=100, d=0):
    for _ in range(n):
        click(gas, t)
        time.sleep(d)

def getscreen():
    os.system("adb exec-out screencap -p > shot.png")

def getstatus():
    getscreen()
    im = Image.open("shot.png")
    if (im.getpixel(start) == (92, 144, 53, 255)):
        return "start"
    if (im.getpixel(pause) == (247, 247, 247, 255)):
        return "gameplay"
    if (im.getpixel(twitter) == (76, 167, 225, 255)):
        return "continue"

def go_to_start():
    status = getstatus()
    if status == "start":
        click(start)
        return
    if status == "gameplay":
        redo()
        return
    continuestart()

def tap_boom():
    # about 400k / 10 mins
    # ie 1 mil = 25mins
    print("at start --------------")
    t0 = datetime.now()
    time.sleep(1)
    click(gas, 300)
    time.sleep(0.4)
    #click(gas, 400)
    #time.sleep(1)
    booms = 0
    while True:
        print(f"boom {booms}", end="\r")
        booms += 1
        click(gas, 3000)
        status = getstatus()
        #print(status)
        if status == "start":
            click(start)
            break
        if status == "continue":
            continuestart()
            break
        #print("still in the game")
    print()
    diff = datetime.now() - t0
    #print("that took about", diff)
    approx_money = diff.total_seconds() * 400_000 / (10 * 60)
    #print(f"so $${approx_money}")
    return approx_money

def moonlander_moon():
    print("at start --------------")
    t0 = datetime.now()
    time.sleep(1)
    click(gas, 300)
    time.sleep(0.4)
    #click(gas, 400)
    #time.sleep(1)
    booms = 0
    while True:
        print(f"boom {booms}", end="\r")
        booms += 1
        click(gas, 9000)
        t_fall = datetime.now()
        died = False
        while (datetime.now() - t_fall).total_seconds() < 10:
            status = getstatus()
            #print(status)
            if status == "start":
                click(start)
                died = True
                break
            if status == "continue":
                continuestart()
                died = True
                break
        if died:
            break
        #print("still in the game")
    print()
    diff = datetime.now() - t0
    #print("that took about", diff)
    approx_money = diff.total_seconds() * 400_000 / (10 * 60)
    #print(f"so $${approx_money}")
    return approx_money


def moonlander_moon_clean():
    print("at start --------------")
    time.sleep(1)
    click(gas, 300)
    time.sleep(0.4)
    click(gas, 9000)
    time.sleep(9)
    redo()
    exact_money = 25000
    return exact_money

def tryit():
    total_profit = 0
    go_to_start()
    while True:
        total_profit += moonlander_moon_clean()
        print("total profit about", total_profit)

tryit()
