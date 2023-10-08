import pygame


class TextBox(object):
    def __init__(self, x, y, w, h, color, maincolor, limiter, txtSize, txt=""):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.txt = txt
        self.color = color
        self.maincolor = maincolor
        self.Done = False
        self.active = False
        self.limiter = limiter
        self.txtSize = txtSize
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def Write(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pass
            elif event.key == pygame.K_BACKSPACE:
                self.txt = self.txt[:-1]
            else:
                self.txt += event.unicode

    def draw(self, collider, surface, click):
        if self.rect.colliderect(collider):
            if click:
                self.active = True
                self.txt = ""
            if self.Done:
                self.active = False
        if not self.rect.colliderect(collider):
            if click:
                self.active = False

        pygame.draw.rect(surface, self.maincolor, (self.x, self.y, self.w, self.h))
        if self.active:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.w, self.h))
            if len(self.txt) > self.limiter:
                txtToScreen(self.txt[len(self.txt) - self.limiter: len(self.txt)], (self.x + 3, self.y + 10),
                            self.txtSize, surface, centered=False)
            else:
                txtToScreen(self.txt, (self.x + 3, self.y + 10), self.txtSize, surface, centered=False)
        else:
            pygame.draw.rect(surface, self.maincolor, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.w, self.h), 2)


class Button(object):
    def __init__(self, x, y, w, h, color1, color2, txt, txtSize, action=False, txtColor=(0, 0, 0), limiter=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color1 = color1
        self.color2 = color2
        self.txt = txt
        self.txtSize = txtSize
        self.action = action
        self.rect = pygame.Rect(self.x, self.y, self.w, self.y)
        self.txtColor = txtColor
        self.limiter = limiter
        self.showcolor = color1

    def draw(self, surface, color=(0, 0, 0), ):
        pygame.draw.rect(surface, self.showcolor, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, color, (self.x, self.y, self.w, self.h), 3)
        txtToScreen(self.txt, (self.x + self.w // 2, self.y + self.h // 2), self.txtSize, surface, color=self.txtColor,
                    centered=True, limiter=self.limiter)

    def mouseover(self, surface, mouserect, click):
        changecolor = self.hit(mouserect)
        if changecolor:
            self.draw(surface)
            if click:
                self.action = True
        else:
            self.draw(surface)

    def hit(self, mouserect):
        if self.x <= mouserect[0] <= self.x + self.w and self.y <= mouserect[1] <= self.y + self.h:
            changecolor = True
            self.showcolor = self.color2
        else:
            changecolor = False
            self.showcolor = self.color1
        return changecolor


def txtToScreen(txt, pos, size, display, color=(0, 0, 0), centered=True, limiter=0):
    font = pygame.font.SysFont(None, size)
    if limiter != 0:
        newtxt = txt[0: limiter]
    else:
        newtxt = txt
    show = font.render(newtxt, True, color)
    if centered:
        new_pos = [pos[0] - show.get_width() // 2, pos[1] - show.get_height() / 2]
    else:
        new_pos = pos
    display.blit(show, new_pos)


def loadpic(path):
    pic = pygame.image.load(path)
    return pic
