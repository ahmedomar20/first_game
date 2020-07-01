import sys, pygame
pygame.init()

pygame.display.set_caption("first game")



#hero movements
walkRight = [pygame.image.load("R1.png"), pygame.image.load("R2.png"), pygame.image.load("R3.png"),
             pygame.image.load("R4.png"), pygame.image.load("R5.png"), pygame.image.load("R6.png"),
             pygame.image.load("R7.png"), pygame.image.load("R8.png"), pygame.image.load("R9.png")]

walkLeft = [pygame.image.load("L1.png"), pygame.image.load("L2.png"), pygame.image.load("L3.png"),
            pygame.image.load("L4.png"), pygame.image.load("L5.png"), pygame.image.load("L6.png"),
            pygame.image.load("L7.png"), pygame.image.load("L8.png"), pygame.image.load("L9.png")]

### defining variables
screen_size = 852, 480
screen = pygame.display.set_mode(screen_size)
# the width and height of the character
width = 64  
height = 64               
screen_width = screen_size[0] - width
screen_height = screen_size[1] - height
background = pygame.image.load("bg.jpg")
char = pygame.image.load("standing.png") 
clock = pygame.time.Clock()
score = 0
# sounds
music = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)


class player(object): 
    def __init__(self, x, y , width, height): 
        self.x = x 
        self.y = y 
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jumping = False
        self.jump_acc = 10
        self.left = False
        self.right = False 
        self.walkcount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win): 
        if self.walkcount + 1 >= 27:
            self.walkcount = 0
        if self.standing == False:
            if self.left:
                screen.blit(walkLeft[self.walkcount//3], (self.x, self.y))
                self.walkcount += 1
            elif self.right:
                screen.blit(walkRight[self.walkcount//3], (self.x, self.y))
                self.walkcount += 1
        else:
            if self.right : 
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
    
    def hit(self): 
        self.is_jumping = False
        self.jump_acc = 10
        self.x = 60 
        self.y = 410
        self.walkcount = 0
        font1 = pygame.font.SysFont("comicsans", 100)
        text = font1.render("0", 1, (255, 0, 0))
        screen.blit(text, (420, 240))
        pygame.display.update()
        i = 0
        while i < 100: 
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
    
                if key[pygame.K_ESCAPE]:
                    sys.exit()
            
                if key[pygame.K_F4]:
                    sys.exit()



class enemy(object): 
    ### enemy movements
    walkLeft_e = [pygame.image.load("L1E.png"), pygame.image.load("L2E.png"), pygame.image.load("L3E.png"),
    pygame.image.load("L4E.png"),pygame.image.load("L5E.png"), pygame.image.load("L6E.png"),pygame.image.load("L7E.png"),
    pygame.image.load("L8E.png"),pygame.image.load("L9E.png"),pygame.image.load("L10E.png"), pygame.image.load("L11E.png")]

    walkRight_e = [pygame.image.load("R1E.png"), pygame.image.load("R2E.png"), pygame.image.load("R3E.png"),
    pygame.image.load("R4E.png"),pygame.image.load("R5E.png"), pygame.image.load("R6E.png"),pygame.image.load("R7E.png"),
    pygame.image.load("R8E.png"),pygame.image.load("R9E.png"),pygame.image.load("R10E.png"), pygame.image.load("R11E.png")]

    def __init__(self, x, y, width, height, end): 
        self.x = x
        self.y = y 
        self.width = width 
        self.height = height 
        self.end = end
        self.path = [self.x, self.end]
        self.walkcount = 0
        self.vel = 3 
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 100
        self.visible = True
    
    def draw(self, win): 
        self.move()
        if self.visible:
            if self.walkcount + 1 >= 33:
                self.walkcount = 0 
            if self.vel > 0: 
                win.blit(self.walkRight_e[self.walkcount // 3], (self.x, self.y) )
                self.walkcount += 1
            else:
                win.blit(self.walkLeft_e[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
            pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(screen, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (0.5 * (100 - self.health)) , 10))
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)


    def move(self): 
        if self.vel > 0: 
            if self.x + self.vel < self.path[1] : 
                self.x += self.vel
            else: 
                self.vel = self.vel * -1
                self.walkcount = 0
        else:
            if self.x - self.vel > self.path[0]: 
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0

    def hit(self): 
        if self.health > 0 :
            self.health -= 1
        else: 
            self.visible = False



class projectile(object): 
    def __init__(self, x, y, radius, color, facing): 
        self.x = x 
        self.y = y 
        self.radius = radius
        self.color = color
        self.facing = facing
        # facing is gonna be negative or positive value to determine the directino of bullets
        self.vel = 8 * facing 

    def draw(self, win): 
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def DrawGameScreen(): 
    screen.blit(background, (0, 0))
    text = font.render("score: " + str(score), 1, (0, 0, 0))
    screen.blit(text, (390, 10))
    man.draw(screen)
    if goblin.health > 0 :
        goblin.draw(screen)
    elif goblin.health <= 0 : 
        goblin.hitbox = (0, 0, 0, 0)
    for bullet in bullets: 
        bullet.draw(screen)
    pygame.display.update()


#main lopp
man = player(300, 410, 64, 64)
goblin = enemy(0+64, 410, 64, 64, 852- 64)
shootLoop = 0
bullets = []
while True:

    clock.tick(40)
    key = pygame.key.get_pressed()
    font = pygame.font.SysFont("comicsans", 30, True)
    
    ### when they collide 
    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                goblin.health = 100
                goblin.x = 600
                goblin.y = 410


    # with open("events2.txt", "a") as events:
    #     for event in pygame.event.get():
    #         events.write(str(event.type)+ "\n")

    if shootLoop > 0: 
        shootLoop += 1 
    if shootLoop > 4: 
        shootLoop = 0

    ### how to close the game 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    if key[pygame.K_ESCAPE]:
        sys.exit()
    
    if key[pygame.K_F4]:
        sys.exit()

    ###bullets
    for bullet in bullets: 
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                hit_sound = pygame.mixer.music.load("hit.mp3")
                pygame.mixer.music.play(0)
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 852 and bullet.x > 0 : 
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    if key[pygame.K_SPACE] and shootLoop == 0: 
        bullet_sound = pygame.mixer.music.load("bullet.mp3")
        pygame.mixer.music.play(0)
        if man.left:
            facing = -1
        else: 
            facing = 1
        if len(bullets) < 10: 
            bullets.append(projectile(round(man.x + man.width // 2 ), round(man.y + man.height //2 ), 6, (0,0,0), facing))
        shootLoop = 1


    ###movements 
    if key[pygame.K_LEFT]:
        if man.x == 0:
            continue
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif key[pygame.K_RIGHT]:
        if man.x == screen_width:
            continue
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.walkcount = 0
        man.standing = True


    #jumping
    if not(man.is_jumping):
        if key[pygame.K_UP]:
            if man.y == 0:
                continue
            man.is_jumping = True
            man.walkcount = 0
    else : 
        if man.jump_acc >= -10:
            neg = 1
            if man.jump_acc < 0:
                neg = -1
            man.y -= (man.jump_acc ** 2) * .5 * neg
            man.jump_acc -= 1
        else : 
            man.is_jumping = False
            man.jump_acc = 10

    DrawGameScreen()
