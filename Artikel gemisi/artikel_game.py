import sys
import time
import  pygame
import random
import pandas as pd
random_finish = 300
random_start = 250
select_time = []
powers = []
num_bullets = 5
healt = 100
damage = 0
score_art = 0


def game(ses):

    global num_bullets
    pygame.init()
    font = pygame.font.SysFont("Times New Roman", 30)
    yazi = font.render("Süre : ", True, (0,255,0))
    level_yazi = font.render("Level : ", True, (0,255,0))
    score_yazi = font.render("Score : ", True, (0,255,0))


    kelime = ""
    t_kelime = ""
    screen = pygame.display.set_mode((1366,768))

    def img(path, size):
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.smoothscale(image, size)
        return image

    ship = img(path = "asset/ship.png" , size =(100,100))
    pygame.display.set_caption("Artikel gemisi")

    def kelimeler(path):
        dosya = pd.read_csv(path)
        türkçe = dosya.iloc[:, 0].values
        artikeller = dosya.iloc[:, 1].values
        kelimeler = dosya.iloc[:, 2].values
        return türkçe, artikeller, kelimeler

    words = kelimeler(path="words")
    artikel = words[1]
    almanca_kelime = words[2]
    türkçe_kelime = words[0]


    der_asteroid_img_path = ["asteroid_asset/AsteroidDer.png", "asteroid_asset/AsteroidDer2.png",
                             "asteroid_asset/AsteroidDer3.png"]
    das_asteroid_img_path = ["asteroid_asset/AsteroidDas.png", "asteroid_asset/AsteroidDas2.png",
                             "asteroid_asset/AsteroidDas3.png"]
    die_asteroid_img_path = ["asteroid_asset/AsteroidDie.png", "asteroid_asset/AsteroidDie2.png",
                             "asteroid_asset/AsteroidDie3.png"]
    der_size = [(138 * 3 / 4, 137 * 3 / 4), (229 * 3 / 4, 240 * 3 / 4), (215 * 3 / 4, 194 * 3 / 4)]
    das_size = [(134 * 3 / 4, 136 * 3 / 4), (181 * 3 / 4, 157 * 3 / 4), (164 * 3 / 4, 155 * 3 / 4)]
    die_size = [(138 * 3 / 4, 138 * 3 / 4), (174 * 3 / 4, 158 * 3 / 4), (215 * 3 / 4, 202 * 3 / 4)]
    der_asteroid_img = []
    das_asteroid_img = []
    die_asteroid_img = []

    def img_convert(path, classe, sizes):
        for p in range(len(path)):
            classe.append(img(path=path[p], size=sizes[p]))

    img_convert(path=der_asteroid_img_path, classe=der_asteroid_img, sizes=der_size)
    img_convert(path=das_asteroid_img_path, classe=das_asteroid_img, sizes=das_size)
    img_convert(path=die_asteroid_img_path, classe=die_asteroid_img, sizes=die_size)
    asteroids = []
    all_images = [der_asteroid_img, die_asteroid_img, das_asteroid_img]

    def random_asteroid(screen, random_num, fasty):
        if (len(asteroids) < random_num):
            s1 = random.randint(0, 2)
            s2 = random.randint(0, 2)
            ran_x = random.randint(0, screen.get_width() - 100)
            y = random.randint(-900, 0)

            asteroids.append([s1, s2, ran_x, y])

        if (len(asteroids) > 0):

            for asteroid in asteroids:
                screen.blit(all_images[asteroid[0]][asteroid[1]], (asteroid[2], asteroid[3]))
                asteroid[3] = asteroid[3] + fasty
                if (asteroid[3] > screen.get_height() + 200):
                    asteroids.remove(asteroid)

    remove_ast = []
    true_counter = 0

    def yok_et(asteroids, screen, lazers):
        if (len(lazers) > 0 and len(asteroids) > 0):
            for ast in asteroids:
                for lazer in lazers:
                    if (screen.blit(all_images[ast[0]][ast[1]], (ast[2], ast[3])).collidepoint(lazer[0], lazer[1])):
                        asteroids.remove(ast)
                        lazers.remove(lazer)
                        lazer_sound = pygame.mixer.Sound("asset/patlama.wav")
                        lazer_sound.set_volume(ses)
                        lazer_sound.play()
                        remove_ast.append(ast)



    def can(asteroids, ship_moves, screen, x, y):
        global healt, damage
        if (len(asteroids) > 0):
            for ship_move in ship_moves:
                for ast in asteroids:

                    if (
                    screen.blit(all_images[ast[0]][ast[1]], (ast[2], ast[3])).collidepoint(ship_move[0], ship_move[1])):
                        asteroids.remove(ast)
                        lazer_sound = pygame.mixer.Sound("asset/damage.mp3")
                        lazer_sound.set_volume(ses)
                        lazer_sound.play()
                        healt = healt - 10
                        damage = damage + 10


        pygame.draw.rect(screen, color=(0, 255, 0), rect=pygame.Rect(x, y, healt, 7))
        pygame.draw.rect(screen, color=(255, 0, 0), rect=pygame.Rect(x + healt, y, damage, 7))

    powers_healt = []

    select_time = []

    def shield_power(clock, moves, screen, fast):
        global random_start, random_finish, num_bullets, healt, damage
        simge = img(path="asset/shield.png", size=(75, 75))
        random_süre = random.randint(random_start, random_finish)
        if len(select_time) == 0:
            select_time.append(random_süre)
            random_finish = random_süre
            random_start = random_finish - 100
        if len(select_time) > 0 and select_time[-1] >= clock:
            ran_x = random.randint(0, screen.get_width() - 100)
            y = random.randint(-900, 0)
            powers_healt.append([ran_x, y])
            select_time.clear()
        if len(powers_healt) > 0:
            for hea in powers_healt:
                screen.blit(simge, (hea[0], hea[1]))
                hea[1] = hea[1] + fast
                if (hea[1] > screen.get_height() + 200):
                    powers_healt.remove(hea)
                for move in moves:
                    if (screen.blit(simge, (hea[0], hea[1])).collidepoint(move[0], move[1])):
                        powers_healt.remove(hea)
                        lazer_sound = pygame.mixer.Sound("asset/true.mp3")
                        lazer_sound.set_volume(ses)
                        lazer_sound.play()
                        healt = healt + 20
                        damage = damage - 20
                        if(healt >= 100):
                            healt = 100
                            damage = 0


    clas = ["der", "die", "das"]

    def score(artikel, asteroids):

        global score_art
        if (len(asteroids) > 0):
            for ast in asteroids:
                if (clas[ast[0]] == artikel):
                    score_art = score_art + 10
                    asteroids.remove(ast)
                else:
                    score_art = score_art - 10
                    asteroids.remove(ast)
    work = True
    bg = img(path ="asset/bg.png" , size = (1366,768))
    w = screen.get_width()
    w_s = ship.get_width()
    w2 = (w-w_s)/2
    h = screen.get_height()
    h_s = ship.get_height()
    h2 = (h-h_s)/2
    fast = 4
    bullets = []
    gösterge_konumlar = [(w-30 , 10),(w-70 , 10),(w-110 , 10),(w-150 , 10),(w-190 , 10)]
    def gösterge(konum):
        image = pygame.image.load("asset/bullet.png").convert_alpha()
        screen.blit(image , konum)
    def lazer(fast  ):
        # bullet[0] = x
         if(len(bullets) > 0):
            for i in range(len(bullets)):
                bullets[i] = [bullets[i][0] ,bullets[i][1] -fast]
                pygame.draw.rect(screen, color=(255, 0, 0), rect=pygame.Rect(bullets[i][0],bullets[i][1], 7, 20),   border_radius=20)

         for bullet in bullets:
           if (bullet[1] < 0):
             bullets.remove(bullet)
    start_time  = time.time()
    start_time2 = 300
    times = [-2,-1]
    times_level = [0]
    times_bullet = [0]

    def bullet_power(clock, moves, screen, fast):
        global random_start, random_finish ,num_bullets
        simge = img(path="asset/simge.png", size=(75, 75))
        random_süre = random.randint(random_start, random_finish)
        if len(select_time) == 0:
            select_time.append(random_süre)
            random_finish = random_süre
            random_start = random_finish - 50
        if len(select_time) > 0 and select_time[-1] >= clock:
            ran_x = random.randint(0, screen.get_width() - 100)
            y = random.randint(-900, 0)
            powers.append([ran_x, y])
            select_time.clear()
        if len(powers) > 0:
            for hea in powers:
                screen.blit(simge, (hea[0], hea[1]))
                hea[1] = hea[1] + fast
                if (hea[1] > screen.get_height() + 200):
                    powers.remove(hea)
                for move in moves :
                 if (screen.blit(simge, (hea[0], hea[1])).collidepoint(move[0], move[1])):
                        powers.remove(hea)
                        lazer_sound = pygame.mixer.Sound("asset/gun.wav")
                        lazer_sound.set_volume(ses)
                        lazer_sound.play()
                        num_bullets = 5
    times_kelime = [-1]
    def clear():
        times_level.clear()
        times_level.append(0)
    fps = 0
    fps_time_start = 0
    while work:
        fps_end = time.time()
        dif = fps_end - fps_time_start
        fps = 1/(dif)
        fps_time_start = fps_end
        print(fps)
        global healt ,damage , score_art
        finis = time.time()
        clock = round(finis - start_time,1)
        clock2 = clock
        clock = start_time2 - clock
        if (times_kelime[-1] != clock and clock % 20 == 0):
            times_kelime.append(clock)
            s1 =  random.randint(0 ,len(almanca_kelime)-1)
            kelime = almanca_kelime[s1]
            t_kelime = türkçe_kelime[s1]
        if (clock < 1 ):
            pygame.display.quit()

            scrd = open(file = "score" , mode="r")
            scr = scrd.readline()
            if (score_art > int(scr) ):
                scrw =open(file = "score" , mode="w")
                scrw.write(str(score_art))
            else:
                scrw = open(file="score", mode="w")
                scrw.write(str(scr))
            clear()
            healt = 100
            damage = 0
            scr2 = score_art
            score_art = 0
            return False , scr2
        if(times_level[-1] != clock and clock%30 == 0):
            times_level.append(clock)
        if(times_bullet[-1] != clock and clock%1.5 == 0 and num_bullets != 5 ):
            times_bullet.append(clock)
            num_bullets = num_bullets + 1

        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                work = False
        screen.blit(bg , (0,0))
        screen.blit(ship , (w2, h2))
        if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
            w2 = w2-  fast
        if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
            w2 = w2+  fast
        if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP]:
            h2 = h2-  fast
        if pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN]:
            h2 = h2 +  fast
        if pygame.key.get_pressed()[pygame.K_SPACE] and len(bullets) < 5 and (clock2 - times[-1]  >= 0.2  and num_bullets != 0) :
            bullets.append([w2+w_s/2 , h2 ])
            lazer_sound= pygame.mixer.Sound("asset/lazer.mp3")
            lazer_sound.set_volume(ses)
            lazer_sound.play()
            times.append(clock2)
            num_bullets  = num_bullets -1
        for i in gösterge_konumlar[0:num_bullets]:
            gösterge(konum=i)
        lazer(fast = 6  )
        if(w2 >w-w_s ):
            w2 = w - w_s
        if (w2 < 0):
            w2 =0
        if(h2 > h-h_s):
            h2 = h-h_s
        if (h2 < 0):
            h2 =0
        yok_et(asteroids=asteroids ,lazers=bullets  , screen=screen )
        random_asteroid(screen=screen, random_num=4 + len(times_level), fasty=0.75 +len(times_level)/10)

        yazi2 = font.render(str(int(clock)), True, (0, 255, 0))
        level_yazi2 = font.render(str(len(times_level)-1), True, (0, 255, 0))

        can( asteroids = asteroids,x =w2, y=h2+h_s+20, ship_moves =[(w2+w_s , h2),(w2 , h2+h_s),(w2 , h2),(w2 + w_s, h2 + h_s),(w2 + w_s/2, h2 + h_s/2)] , screen = screen)
        bullet_power(clock = clock ,moves=[(w2+w_s , h2),(w2 , h2+h_s),(w2 , h2),(w2 + w_s, h2 + h_s),(w2 + w_s/2, h2 + h_s/2)] ,screen=screen ,fast=1)
        shield_power( clock = clock ,moves=[(w2+w_s , h2),(w2 , h2+h_s),(w2 , h2),(w2 + w_s, h2 + h_s),(w2 + w_s/2, h2 + h_s/2)] ,screen=screen ,fast=1)

        screen.blit(yazi, (10, 10))
        screen.blit(level_yazi, (10, 40))
        screen.blit(level_yazi2, (100, 40))
        screen.blit(yazi2, (90, 10))
        screen.blit(score_yazi, (10, 75))
        score(artikel=artikel[s1] , asteroids=remove_ast)
        if healt <= 0:
            pygame.display.quit()
            clear()
            healt = 100
            damage = 0
            scr2 = score_art
            score_art = 0
            return False , scr2
        yazi_score = font.render(str(score_art), True, (0, 255, 0))
        screen.blit(yazi_score, (100, 75))
        if (times_level[-1] == " "):
         yazi5 = font.render(kelime+"("+t_kelime[-1]+")", True, (255, 255, 200))
        else:
         yazi5 = font.render(kelime + "(" + t_kelime + ")", True, (255, 255, 200))

        rect = pygame.Rect(((w-400)/2,0), (400, 50))
        start_rect = yazi5.get_rect(center=rect.center)
        pygame.draw.rect(screen, color="#808080", rect=pygame.Rect((w-400)/2,0, 400, 50),)
        screen.blit(yazi5, start_rect)

        pygame.display.update()
