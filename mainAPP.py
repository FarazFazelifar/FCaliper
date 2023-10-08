import math
import os
import sys

from GameEngine import *

os.environ['SDL_VIDEO_WINDOW_POS'] = '%d, %d' % (1080, 960)
os.environ['SDL_VIDEO_CENTERED'] = '0'

pygame.init()
pygame.font.init()

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
width, height = width // 2, height // 2

timetxt = 'Duration: {} mSec'
zoomtxt = 'Zoom: {} X'
amptxt = 'Amp: {} mm'
sumtxt = 'sum: {}'
abssum = 'abssum: {}'
stxt = 'S{no} : {surface}'
location = ''
startmesuring = False
init = False
firstmesure = True
movepic = False
mesure = (0, 0, 0, 0)
surfaceareas = []
keypresses = []
mesures = []
dots = []
dotsArray = []
zoom = 1
imgAvailable = False
retry = True
clock = pygame.time.Clock()
activemesure = 0
helpScreen = False
formulasScreen = False
pic = newpic = picx = picy = imgAvailable = location = 0
bazzetQT = bazzetRR = fridQT = fridRR = lvhL = lvhR = hodgeQT = hodgeRR = bazzetQtc = heartRateRR =0

f = open("path.txt", 'r')
if f.readline() == '':
    sys.exit()

window = pygame.Surface((1080, 920))
Display = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Heart Caliper")
abspath = os.path.abspath(__file__)
abspath = abspath[:-11]


def zoomInPic(pic, mesures):
    w = pic.get_width() * 2
    h = pic.get_height() * 2
    pic = pygame.transform.scale(pic, (w, h))
    for i in range(len(mesures)):
        mesures[i][0][2] *= 2
        mesures[i][0][3] *= 2
        mesures[i][0][0] = picx + (mesures[i][0][0] - picx) * 2
        mesures[i][0][1] = picy + (mesures[i][0][1] - picy) * 2
    for d in dotsArray:
        for i in range(len(d)):
            x = d[i][0]
            y = d[i][1]
            x = picx + (x - picx) * 2
            y = picy + (y - picy) * 2
            d[i] = (x, y)
    for i in range(len(dots)):
        x = dots[i][0]
        y = dots[i][1]
        x = picx + (x - picx) * 2
        y = picy + (y - picy) * 2
        dots[i] = (x, y)

    return pic


def zoomOutPic(pic, mesures):
    w = pic.get_width() // 2
    h = pic.get_height() // 2
    pic = pygame.transform.scale(pic, (w, h))
    for i in range(len(mesures)):
        mesures[i][0][2] /= 2
        mesures[i][0][3] /= 2
        mesures[i][0][0] += (picx - mesures[i][0][0]) / 2
        mesures[i][0][1] += (picy - mesures[i][0][1]) / 2
    for d in dotsArray:
        for i in range(len(d)):
            x = d[i][0]
            y = d[i][1]
            x += (picx - x) / 2
            y += (picy - y) / 2
            d[i] = (x, y)
    for i in range(len(dots)):
        x = dots[i][0]
        y = dots[i][1]
        x += (picx - x) / 2
        y += (picy - y) / 2
        dots[i] = (x, y)
    return pic


def SurfaceArea(surfacearea, dots):
    if len(dots) >= 2:
        if dots[-1][1] < dots[-2][1]:
            thirdDot = (dots[-1][0], dots[-2][1])
            h = dots[-1][1] - thirdDot[1]
            w = thirdDot[0] - dots[-2][0]
            s = h * w / 2
            surfacearea += s

        else:
            thirdDot = (dots[-2][0], dots[-1][1])
            h = dots[-2][1] - thirdDot[1]
            w = dots[-1][0] - thirdDot[0]
            s = h * w / 2
            surfacearea += s
        pygame.draw.line(Display, (255, 0, 0), dots[-2], dots[-1], 3)
        pygame.draw.line(Display, (0, 255, 0), dots[-2], thirdDot, 3)
        pygame.draw.line(Display, (0, 0, 255), thirdDot, dots[-1], 3)

    return dots, surfacearea


def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size)
    shape_surf.set_alpha(96)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    shape_surf.set_colorkey((0, 0, 0))
    surface.blit(shape_surf, target_rect)


def open_file(pic, newpic, picx, picy, imgAvailable, location):
    if os.path.exists("path.txt"):
        f = open("path.txt", "r")
        location = f.readline()
        f.close()
        if location != '':
            try:
                pic = loadpic(location)
            except:
                sys.exit()
            newpic = pic
            picx = (1080 - newpic.get_width()) // 2
            picy = (920 - newpic.get_height()) // 2
            imgAvailable = True
        return pic, newpic, picx, picy, imgAvailable, location
    else:
        return pic, newpic, picx, picy, imgAvailable, location


def save_file(mesures, surfaceareas, location):
    desktop = os.path.join(os.environ["HOMEPATH"], "Desktop")
    os.chdir(desktop)
    if os.path.exists(desktop + "/FCaliper Saved Files"):
        os.chdir(desktop + "\FCaliper Saved Files")
        curdir = os.path.abspath(os.path.curdir)
        print(str(curdir))
        f = open(location[location.rfind("/") + 1: len(location)] + ".txt", "w")
        f.write(location)
        f.write("\n")
        for i in range(len(mesures) - 1):
            displayNT = mesures[i + 1][2][0] / mesures[0][2][0]
            displayNT *= 200
            displayNT = math.floor(displayNT * 10) / 10
            displayNA = mesures[i + 1][2][1] / mesures[0][2][1]
            displayNA *= 5
            displayNA = math.floor(displayNA * 10) / 10
            f.write(
                "Measure #" + str(i + 1) + " : Duration = " + str(abs(displayNT)) + " | Amplitude = " + str(displayNA))
            f.write("\n")
        f.write("_____________________________________________________")
        f.write("\n")
        for i in range(len(surfaceareas)):
            f.write("S #" + str(i + 1) + " : " + str(surfaceareas[i]))
            f.write("\n")
    else:
        os.chdir(desktop)
        os.mkdir(desktop + "/FCaliper Saved Files")
        save_file(mesures, surfaceareas, location)


openButton = Button(0, 0, 100, 25, (158, 158, 158), (224, 224, 224), "Open", 20)
helpButton = Button(100, 0, 100, 25, (158, 158, 158), (224, 224, 224), "Help", 20)
saveButton = Button(200, 0, 100, 25, (158, 158, 158), (224, 224, 224), "Save", 20)
formulasButton = Button(300, 0, 100, 25, (158, 158, 158), (224, 224, 224), "Formulas", 20)

txtBoxBazzettQT = TextBox(278, 265, 150, 50, (100, 100, 100), (255, 255, 255), 9, 40)
txtBoxBazzettRR = TextBox(490, 265, 150, 50, (100, 100, 100), (255, 255, 255), 9, 40)
txtBoxFridQT = TextBox(278, 365, 150, 50, (100, 100, 100), (255, 255, 255), 9, 40)
txtBoxFridRR = TextBox(490, 365, 150, 50, (100, 100, 100), (255, 255, 255), 9, 40)
txtBoxLvhL = TextBox(278, 165, 150, 50, (100, 100, 100), (255, 255, 255), 9, 40)
txtBoxLvhR = TextBox(490, 165, 150, 50, (100, 100, 100), (255, 255, 255), 9, 40)
txtBoxHodgeQT = TextBox(278, 465, 150, 50, (100, 100, 100), (255, 255, 255), 9, 40)
txtBoxHodgeRR = TextBox(490, 465, 150, 50, (100, 100, 100), (255, 255, 255), 9, 40)
txtBoxHeartRate = TextBox(278, 65, 150, 50, (100, 100, 100), (255, 255, 255), 9, 40)


while True:
    os.chdir(abspath)
    clock.tick(144)
    # window.fill((242, 242, 242))
    Display.fill((200, 200, 200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if helpScreen and formulasScreen:
            txtBoxBazzettQT.Write(event)
            txtBoxBazzettRR.Write(event)
            txtBoxFridQT.Write(event)
            txtBoxFridRR.Write(event)
            txtBoxLvhL.Write(event)
            txtBoxLvhR.Write(event)
            txtBoxHodgeQT.Write(event)
            txtBoxHodgeRR.Write(event)
            txtBoxHeartRate.Write(event)

        if not helpScreen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not keypresses[pygame.K_LSHIFT]:
                    if imgAvailable:
                        startmesuring = True

                if event.button == 4 and keypresses[pygame.K_LCTRL]:
                    if zoom * 2 <= 8 and newpic.get_width() * 2 < 12000 and newpic.get_height() * 2 < 12000:
                        zoom *= 2
                        newpic = zoomInPic(newpic, mesures)

                if event.button == 5 and keypresses[pygame.K_LCTRL]:
                    if zoom / 2 >= 1:
                        zoom /= 2
                        newpic = zoomOutPic(newpic, mesures)

                if event.button == 3:
                    movepic = True

                if event.button == 1 and keypresses[pygame.K_LSHIFT]:
                    if len(mesures) > 0:
                        dots.append(mousepos)
                        pygame.time.delay(175)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button != 4:
                    if event.button != 5:
                        if event.button == 1 and not keypresses[pygame.K_LSHIFT]:
                            if firstmesure:
                                if imgAvailable:
                                    firstmesure = not firstmesure

                if event.button == 1 and not keypresses[pygame.K_LSHIFT]:
                    if firstmesure == False:
                        oringinalsize = (mesure[2], mesure[3])
                        tm = mesure[2] * (8 / zoom)
                        am = mesure[3] * (8 / zoom)
                        mesures.append([mesure, oringinalsize, [tm, am]])
                        activemesure = len(mesures) - 1

                    startmesuring = False
                    init = False
                    mesure = (0, 0, 0, 0)

                if event.button == 3:
                    movepic = False

        if event.type == pygame.VIDEORESIZE:
            Display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    if retry:
        pic, newpic, picx, picy, imgAvailable, location = open_file(pic, newpic, picx, picy, imgAvailable, location)
        retry = False

    mousepos = pygame.mouse.get_pos()
    mousex, mousey = mousepos
    keypresses = pygame.key.get_pressed()
    mousemove = pygame.mouse.get_rel()
    mousex += mousemove[0]
    mousey += mousemove[1]
    mouseClick = pygame.mouse.get_pressed()
    if mouseClick[0] == 1:
        click = True
    else:
        click = False

    if not helpScreen:
        if keypresses[pygame.K_RIGHT]:
            if activemesure + 1 <= len(mesures) - 1:
                activemesure += 1
                pygame.time.delay(200)

        if keypresses[pygame.K_LEFT]:
            if activemesure - 1 > 0:
                activemesure -= 1
                pygame.time.delay(200)

        if keypresses[pygame.K_LCTRL] and keypresses[pygame.K_z]:
            if activemesure == len(mesures) - 1:
                activemesure = len(mesures) - 2
            if len(mesures) - 1 >= 0:
                mesures.pop()
                pygame.time.delay(200)
                if len(mesures) == 0:
                    dots = []

        if keypresses[pygame.K_LSHIFT] and keypresses[pygame.K_z]:
            if len(dots) > 0:
                dots = []
            elif len(dots) == 0:
                surfaceareas.pop()
                dotsArray.pop()
            pygame.time.delay(200)

        if firstmesure == False:
            if startmesuring:
                if init == False:
                    initpos = mousepos
                mesure = pygame.Rect((initpos[0], initpos[1], mousepos[0] - initpos[0], mousepos[1] - initpos[1]))
                init = True

        else:
            if startmesuring:
                if init == False:
                    initpos = mousepos
                mesure = pygame.Rect((initpos[0], initpos[1], mousepos[0] - initpos[0], mousepos[1] - initpos[1]))
                init = True

        if movepic:
            picx += mousemove[0]
            picy += mousemove[1]
            if len(mesures) > 0:
                for mesure in mesures:
                    mesure[0][0] += mousemove[0]
                    mesure[0][1] += mousemove[1]
            for d in dotsArray:
                for i in range(len(d)):
                    x = d[i][0]
                    y = d[i][1]
                    x += mousemove[0]
                    y += mousemove[1]
                    d[i] = (x, y)
            for i in range(len(dots)):
                x = dots[i][0]
                y = dots[i][1]
                x += mousemove[0]
                y += mousemove[1]
                dots[i] = (x, y)

        Display.blit(newpic, (picx, picy))

        if not firstmesure:
            try:
                try:
                    displayNT = mesures[activemesure][2][0] / mesures[0][2][0]
                    displayNT *= 200
                    displayNT = math.floor(displayNT * 10) / 10
                    txtToScreen(timetxt.format(abs(displayNT)), (20, Display.get_height() - 100), 40, Display,
                                centered=False, color=(0, 51, 0))
                    displayNA = mesures[activemesure][2][1] / mesures[0][2][1]
                    displayNA *= 5
                    displayNA = math.floor(displayNA * 10) / 10
                    txtToScreen(amptxt.format(abs(displayNA)), (20, Display.get_height() - 50), 40, Display,
                                centered=False, color=(0, 51, 0))
                except:
                    pass
            except:
                firstmesure = True

        if not firstmesure:
            if len(dots) > 2 and len(mesures) > 0:
                draw_polygon_alpha(Display, (128, 204, 255), dots)
                pygame.draw.polygon(Display, (0, 107, 179), dots, 2)

                plus = minus = 0

                for i in range(len(dots)):
                    plus += dots[i - 1][0] * dots[i][1]
                    minus -= dots[i - 1][1] * dots[i][0]

                sa = plus + minus
                sa /= 2
                sa /= mesures[0][2][0]
                sa /= mesures[0][2][1]
                sa *= 25
                sa = -sa
                sa *= 8 / zoom
                sa *= 8 / zoom
                sa = math.floor(sa * 10) / 10

                if keypresses[pygame.K_RETURN]:
                    surfaceareas.append(sa)
                    dotsArray.append(dots)
                    dots = []
                    pygame.time.delay(200)

        if len(surfaceareas) >= 1:
            txtToScreen(abssum.format(math.floor((sum(abs(x) for x in surfaceareas) * 10)) / 10) + " mm²", (220, 40), 30,
                        Display, (0, 0, 0), False)
            txtToScreen(sumtxt.format(math.floor(sum(surfaceareas) * 10) / 10) + " mm²", (410, 40), 30, Display,
                        (0, 0, 0),
                        False)
            for d in dotsArray:
                draw_polygon_alpha(Display, (128, 204, 255), d)
                pygame.draw.polygon(Display, (0, 107, 179), d, 2)

        if len(surfaceareas) >= 1:
            if len(surfaceareas) >= 5:
                for i in range(5):
                    txtToScreen(
                        stxt.format(no=len(surfaceareas) - 5 + i + 1,
                                    surface=surfaceareas[len(surfaceareas) - 5 + i]) + " mm²",
                        (40, 40 * (i + 1)), 30, Display, centered=False)
            else:
                for i in range(len(surfaceareas)):
                    txtToScreen(stxt.format(no=i + 1, surface=surfaceareas[i]) + " mm²", (40, 40 * (i + 1)), 30, Display,
                                centered=False)

        txtToScreen(zoomtxt.format(zoom), (20, Display.get_height() - 150), 40, Display, centered=False)
        pygame.draw.rect(Display, (0, 0, 0), (0, 0, Display.get_width(), Display.get_height()), 6)

        if len(mesures) > 0:
            for i in range(1, len(mesures)):
                pygame.draw.line(Display, (200, 20, 20), (mesures[i][0][0], mesures[i][0][1]),
                                 (mesures[i][0][0], mesures[i][0][1] + mesures[i][0][3]), 3)
                pygame.draw.line(Display, (200, 20, 20), (mesures[i][0][0], mesures[i][0][1] + mesures[i][0][3]),
                                 (mesures[i][0][0] + mesures[i][0][2], mesures[i][0][1] + mesures[i][0][3]), 3)

            pygame.draw.line(Display, (0, 102, 34), (mesures[activemesure][0][0], mesures[activemesure][0][1]),
                             (mesures[activemesure][0][0], mesures[activemesure][0][1] + mesures[activemesure][0][3]),
                             3)
            pygame.draw.line(Display, (0, 102, 34),
                             (mesures[activemesure][0][0], mesures[activemesure][0][1] + mesures[activemesure][0][3]),
                             (mesures[activemesure][0][0] + mesures[activemesure][0][2],
                              mesures[activemesure][0][1] + mesures[activemesure][0][3]), 3)

            pygame.draw.line(Display, (102, 0, 204), (mesures[0][0][0], mesures[0][0][1]),
                             (mesures[0][0][0], mesures[0][0][1] + mesures[0][0][3]), 3)
            pygame.draw.line(Display, (102, 0, 204),
                             (mesures[0][0][0], mesures[0][0][1] + mesures[0][0][3]),
                             (mesures[0][0][0] + mesures[0][0][2],
                              mesures[0][0][1] + mesures[0][0][3]), 3)

        pygame.draw.rect(Display, (102, 0, 204), (Display.get_width() - 50, Display.get_height() - 165, 20, 20))
        pygame.draw.rect(Display, (0, 0, 0), (Display.get_width() - 50, Display.get_height() - 165, 20, 20), 2)
        pygame.draw.rect(Display, (0, 102, 34), (Display.get_width() - 50, Display.get_height() - 115, 20, 20))
        pygame.draw.rect(Display, (0, 0, 0), (Display.get_width() - 50, Display.get_height() - 115, 20, 20), 2)
        pygame.draw.rect(Display, (200, 20, 20), (Display.get_width() - 50, Display.get_height() - 65, 20, 20))
        pygame.draw.rect(Display, (0, 0, 0), (Display.get_width() - 50, Display.get_height() - 65, 20, 20), 2)
        pygame.draw.rect(Display, (158, 158, 158), (0, 0, Display.get_width(), 25))
        pygame.draw.rect(Display, (0, 0, 0), (0, 0, Display.get_width(), 25), 3)

        txtToScreen('Unit', (Display.get_width() - 90, Display.get_height() - 152), 30, Display)
        txtToScreen('Active Measure', (Display.get_width() - 140, Display.get_height() - 102), 30, Display)
        txtToScreen('Inactive Measure', (Display.get_width() - 150, Display.get_height() - 52), 30, Display)
        # txtToScreen(abspath, (300, 300), 30, Display, centered=False)
        for i in range(len(surfaceareas)):
            txtToScreen(str(i+1), dotsArray[i][0], 30, Display, (200, 45, 45))

        openButton.mouseover(Display, (mousex, mousey, 16, 16), click)
        openButton.draw(Display)
        helpButton.mouseover(Display, (mousex, mousey, 16, 16), click)
        helpButton.draw(Display)
        saveButton.mouseover(Display, (mousex, mousey, 16, 16), click)
        saveButton.draw(Display)
        formulasButton.mouseover(Display, (mousex, mousey, 16, 16), click)
        formulasButton.draw(Display)

        if openButton.action:
            os.system("browser.exe")
            pic, newpic, picx, picy, imgAvailable, location = open_file(pic, newpic, picx, picy, imgAvailable, location)
            retry = False
            openButton.action = False
            firstmesure = True
            surfaceareas = []
            mesures = []
            dots = []
            zoom = 1

        if len(mesures) > 0:
            for i in range(len(mesures)):
                if mesures[i][0][2] == 0 and mesures[i][0][3] == 0:
                    del mesures[i]
                    activemesure -= 1

        if helpButton.action:
            helpScreen = True
            helpButton.action = False

        if saveButton.action:
            saveButton.action = False
            save_file(mesures, surfaceareas, location)

        if formulasButton.action:
            helpScreen = True
            formulasScreen = True
            formulasButton.action = False
    
    elif formulasScreen:
        

        if bazzetRR != 0 and bazzetQT != 0:
            bazzetQtc = math.floor(((bazzetQT / (bazzetRR ** 0.5)) * (1000 ** 0.5)) * 100) / 100
            if bazzetQT >= 470:
                txtToScreen("QTc = {}".format(bazzetQtc), (645, 275), 40, Display, centered=False, color=(255, 50, 50))
            else:
                txtToScreen("QTc = {}".format(bazzetQtc), (645, 275), 40, Display, centered=False)
        else:
            txtToScreen("QTc = 0", (645, 275), 40, Display, centered=False)
        txtToScreen("Bazzet formula: QT=", (0,275), 40, Display, centered=False)
        txtToScreen("RR=", (430, 275), 40, Display, centered=False)

        if fridRR != 0 and fridQT != 0:
            fridQtc = (math.floor((fridQT / (fridRR ** (1 / 3))) * 100) / 100) * 10
            if fridQtc >= 470:
                txtToScreen("QTc = {}".format(fridQtc), (645, 375), 40, Display, centered=False, color=(255, 50, 50))
            else:
                txtToScreen("QTc = {}".format(fridQtc), (645, 375), 40, Display, centered=False)
        else:
            txtToScreen("QTc = 0", (645, 375), 40, Display, centered=False)
        txtToScreen("Fridericia formula: QT=", (0,376), 36, Display, centered=False)
        txtToScreen("RR=", (430, 375), 40, Display, centered=False)

        if lvhL != 0 and lvhR != 0:
            lvh = (math.floor((lvhL+lvhR)*100))/100
            if lvh >= 35:
                txtToScreen("LVH = {}".format(lvh), (645, 175), 40, Display, centered=False, color=(255, 50, 50))
            else:
                txtToScreen("LVH = {}".format(lvh), (645, 175), 40, Display, centered=False)
        else:
            txtToScreen("LVH = 0", (645, 175), 40, Display, centered=False)
        txtToScreen("LVH: S_V2=", (122, 176), 40, Display, centered=False)
        txtToScreen("S_V5=", (430, 181), 30, Display, centered=False)

        if hodgeQT != 0 and hodgeRR != 0:
            hodgeQtc = math.floor((hodgeQT + (((60000 / hodgeRR) - 60)) * 1.75) * 100) / 100
            if hodgeQtc >= 470:
                txtToScreen("QTc = {}".format(hodgeQtc), (645, 475), 40, Display, centered=False, color=(255, 50, 50))
            else:
                txtToScreen("QTc = {}".format(hodgeQtc), (645, 475), 40, Display, centered=False)
        else:
            txtToScreen("QTc = 0", (645, 475), 40, Display, centered=False)
        txtToScreen("Hodges formula: QT=", (0,476), 39, Display, centered=False)
        txtToScreen("RR=", (430, 475), 40, Display, centered=False)

        if heartRateRR != 0:
            heartRate = math.floor((6000000 / heartRateRR)) / 100
            if 60 <= heartRate <= 100:
                txtToScreen("heart rate = {}".format(heartRate), (430, 75), 40, Display, centered=False)
            else:
                txtToScreen("heart rate = {}".format(heartRate), (430, 75), 40, Display, centered=False, color=(255, 50, 50))
        else:
            txtToScreen("heart rate = 0", (450, 75), 40, Display, centered=False)
        txtToScreen("Heart rate: RR=", (71,76), 39, Display, centered=False)

        if txtBoxBazzettQT.active:
            if keypresses[pygame.K_RETURN]:
                bazzetQT = float(txtBoxBazzettQT.txt)
                txtBoxBazzettQT.active = False

        if txtBoxBazzettRR.active:
            if keypresses[pygame.K_RETURN]:
                bazzetRR = float(txtBoxBazzettRR.txt)
                txtBoxBazzettRR.active = False

        if txtBoxLvhL.active:
            if keypresses[pygame.K_RETURN]:
                lvhL = float(txtBoxLvhL.txt)
                txtBoxLvhL.active = False

        if txtBoxLvhR.active:
            if keypresses[pygame.K_RETURN]:
                lvhR = float(txtBoxLvhR.txt)
                txtBoxLvhR.active = False

        if txtBoxFridQT.active:
            if keypresses[pygame.K_RETURN]:
                fridQT = float(txtBoxFridQT.txt)
                txtBoxFridQT.active = False

        if txtBoxFridRR.active:
            if keypresses[pygame.K_RETURN]:
                fridRR = float(txtBoxFridRR.txt)
                txtBoxFridRR.active = False

        if txtBoxHodgeQT.active:
            if keypresses[pygame.K_RETURN]:
                hodgeQT = float(txtBoxHodgeQT.txt)
                txtBoxHodgeQT.active = False

        if txtBoxHodgeRR.active:
            if keypresses[pygame.K_RETURN]:
                hodgeRR = float(txtBoxHodgeRR.txt)
                txtBoxHodgeRR.active = False

        if txtBoxHeartRate.active:
            if keypresses[pygame.K_RETURN]:
                heartRateRR = float(txtBoxHeartRate.txt)
                txtBoxHeartRate.active = False

        txtBoxBazzettQT.draw((mousex, mousey, 16, 16), Display, click)
        txtBoxBazzettRR.draw((mousex, mousey, 16, 16), Display, click)
        txtBoxFridQT.draw((mousex, mousey, 16, 16), Display, click)
        txtBoxFridRR.draw((mousex, mousey, 16, 16), Display, click)
        txtBoxLvhL.draw((mousex, mousey, 16, 16), Display, click)
        txtBoxLvhR.draw((mousex, mousey, 16, 16), Display, click)
        txtBoxHodgeQT.draw((mousex, mousey, 16, 16), Display, click)
        txtBoxHodgeRR.draw((mousex, mousey, 16, 16), Display, click)
        txtBoxHeartRate.draw((mousex, mousey, 16, 16), Display, click)

        if not txtBoxBazzettQT.active:
            txtToScreen(str(bazzetQT), ((txtBoxBazzettQT.x + txtBoxBazzettQT.w + txtBoxBazzettQT.x) // 2, (txtBoxBazzettQT.y + txtBoxBazzettQT.h + txtBoxBazzettQT.y) // 2), 40, Display, limiter=9)
        if not txtBoxBazzettRR.active:
            txtToScreen(str(bazzetRR), ((txtBoxBazzettRR.x + txtBoxBazzettRR.w + txtBoxBazzettRR.x) // 2, (txtBoxBazzettRR.y + txtBoxBazzettRR.h + txtBoxBazzettRR.y) // 2), 40, Display, limiter=9)

        if not txtBoxFridQT.active:
            txtToScreen(str(fridQT), ((txtBoxFridQT.x + txtBoxFridQT.w + txtBoxFridQT.x) // 2, (txtBoxFridQT.y + txtBoxFridQT.h + txtBoxFridQT.y) // 2), 40, Display, limiter=9)
        if not txtBoxFridRR.active:
            txtToScreen(str(fridRR), ((txtBoxFridRR.x + txtBoxFridRR.w + txtBoxFridRR.x) // 2, (txtBoxFridRR.y + txtBoxFridRR.h + txtBoxFridRR.y) // 2), 40, Display, limiter=9)

        if not txtBoxLvhL.active:
            txtToScreen(str(lvhL), ((txtBoxLvhL.x + txtBoxLvhL.w + txtBoxLvhL.x) // 2, (txtBoxLvhL.y + txtBoxLvhL.h + txtBoxLvhL.y) // 2), 40, Display, limiter=9)
        if not txtBoxLvhR.active:
            txtToScreen(str(lvhR), ((txtBoxLvhR.x + txtBoxLvhR.w + txtBoxLvhR.x) // 2, (txtBoxLvhR.y + txtBoxLvhR.h + txtBoxLvhR.y) // 2), 40, Display, limiter=9)

        if not txtBoxHodgeQT.active:
            txtToScreen(str(hodgeQT), ((txtBoxHodgeQT.x + txtBoxHodgeQT.w + txtBoxHodgeQT.x) // 2, (txtBoxHodgeQT.y + txtBoxHodgeQT.h + txtBoxHodgeQT.y) // 2), 40, Display, limiter=9)
        if not txtBoxHodgeRR.active:
            txtToScreen(str(hodgeRR), ((txtBoxHodgeRR.x + txtBoxHodgeRR.w + txtBoxHodgeRR.x) // 2, (txtBoxHodgeRR.y + txtBoxHodgeRR.h + txtBoxHodgeRR.y) // 2), 40, Display, limiter=9)

        if not txtBoxHeartRate.active:
            txtToScreen(str(heartRateRR), ((txtBoxHeartRate.x + txtBoxHeartRate.w + txtBoxHeartRate.x) // 2, (txtBoxHeartRate.y + txtBoxHeartRate.h + txtBoxHeartRate.y) // 2), 40, Display, limiter=9)

        if keypresses[pygame.K_ESCAPE]:
            formulasScreen = False
            helpScreen = False

    else:
        t = open('help.txt', 'rt')
        i = 1
        for line in t:
            txtToScreen(line, (Display.get_width() // 2, 40 * i), 28, Display)
            i += 1
        if keypresses[pygame.K_ESCAPE]:
            helpScreen = False

    pygame.display.flip()
