import pygame
import time
from artikel_game import game

img_s = 0
images = ["asset/s1.png","asset/s2.png","asset/s3.png","asset/s4.png"]
images2 = []

def menü(hıgh_score , score):
    pygame.init()
    screen = pygame.display.set_mode((1366 , 768))
    pygame.display.set_caption("kordinasyon")

    class Button():
        def __init__(self, pos, pos2, color, text, text2, w, h, color2, color3):
            self.color3 = color3
            self.pos = pos
            self.pos2 = pos2
            self.text = text
            self.text2 = text2
            self.w = w
            self.h = h
            self.color = color
            self.color2 = color2

        def button1(self):
            font = pygame.font.SysFont("Times New Roman", 30)
            rect = pygame.Rect(self.pos, (self.w, self.h))

            if (rect.collidepoint(pygame.mouse.get_pos())):
                pygame.draw.rect(screen, self.color3, rect, border_radius=12)
                start = font.render(self.text, True, self.color2)
                start_rect = start.get_rect(center=rect.center)
                screen.blit(start, start_rect)
                if (pygame.mouse.get_pressed()[0]):
                    time.sleep(0.1)
                    return 1
                else:
                    return 0
            else:
                pygame.draw.rect(screen, self.color, rect, border_radius=12)
                start = font.render(self.text, True, self.color2)
                start_rect = start.get_rect(center=rect.center)
                screen.blit(start, start_rect)

        def button2(self):
            font = pygame.font.SysFont("Times New Roman", 30)
            rect = pygame.Rect(self.pos2, (self.w, self.h))

            if (rect.collidepoint(pygame.mouse.get_pos())):
                pygame.draw.rect(screen, self.color3, rect, border_radius=12)
                start = font.render(self.text2, True, self.color2)
                start_rect = start.get_rect(center=rect.center)
                screen.blit(start, start_rect)
                if (pygame.mouse.get_pressed()[0]):
                    time.sleep(0.1)
                    return 1
                else:

                    return 0
            else:
                pygame.draw.rect(screen, self.color, rect, border_radius=12)
                start = font.render(self.text2, True, self.color2)
                start_rect = start.get_rect(center=rect.center)
                screen.blit(start, start_rect)

    def img(path, size):
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.smoothscale(image, size)
        return image

    for i in images:
        images2.append(img(path=i, size=(75, 75)))
    font = pygame.font.SysFont("Times New Roman", 40)
    bg = img(path ="asset/bg.png" , size = (1366,768))
    yazi = font.render("Score : ", True, (0, 255, 0))
    yazi2 = font.render("Hıgh Score : ", True, (0, 255, 0))
    score_t=font.render(str(score), True, (0, 255, 0))
    h_score=font.render(str(hıgh_score), True, (0, 255, 0))
    def set_volume(move , koor):
        global img_s
        if screen.blit(images2[img_s] , move).collidepoint(koor) and pygame.mouse.get_pressed()[0]:
            img_s = img_s+1
            time.sleep(0.3)
        if (img_s >= 4 ):
            img_s = 0
        screen.blit(images2[img_s] , move)
    work  = True
    while work:

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                work = False

        screen.blit(bg , (0,0))
        button = Button(pos=((screen.get_width()-150)/2 , 325), pos2=((screen.get_width()-150)/2 , 425), color="#475F77", color2="#FFFFFF", color3="#D74B4B", text="START",
                        text2="EXİT", w=150, h=40)
        screen.blit(yazi , (600 ,150))
        screen.blit(yazi2 , (600 ,200))
        screen.blit(score_t, (720, 150))
        screen.blit(h_score, (810, 200))
        bsd = button.button1()
        bds2 = button.button2()
        set_volume(move= ((screen.get_width()-150)/2+50 , 500) ,koor=pygame.mouse.get_pos())
        if (bsd == 1):
            return  True , img_s
        if (bds2 == 1):
            pygame.quit()
            return False
        pygame.display.update()
        pygame.display.flip()
def score_read():
    dosya = open("score" , mode="r")
    sc = dosya.readline()
    return sc
import sys
def artikel_game(score ):

    isplayed = menü(score=score , hıgh_score=score_read())
    if isplayed[0] == True:
        isplayed2 = game(ses = isplayed[1]*0.3)
        if(isplayed2[0] == False):
            return artikel_game(score = isplayed2[1])
    else :
        sys.exit()
artikel_game(score="")

