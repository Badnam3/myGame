# -*- coding: cp1252 -*-
from Tkinter import *
import random
import time

"""
todo


LAG ET MAP
farger
1,2,3 kan gi powerup feks større skudd for 10 sec, med 5 min cd ?
penger, items, upgrades
bedre hitbox på skudd
enemies rister litt :/
kanke forandre width og height uten at ting blir rart

"""

enemies = []
width = 800
height = 800


level = {'level':0,'active':False,
                'level_1': {'type1':2},
                'level_2': {'type1':5},
                'level_3': {'type1':10},
                'level_4': {'type2':5},
                'level_5': {'type1':5,'type2':5},
                'level_6': {'type1':10,'type2':10},
                'level_7': {'type1':30},
                'level_8': {'type3':1},
                'level_9': {'type1':3, 'type2':3, 'type3':2},
                'level_10': {'type4':1},
                'level_11': {'type1':10, 'type2':10, 'type3':2},
                'level_12': {'type2':30},
                'level_13': {'type5':2},
                'level_14': {'type2':5, 'type3':3, 'type5':5},
                'level_15': {'type5':20},
                'level_16': {'type1':100},
                'level_17': {'type7':5},
                'level_18': {'type1':20, 'type7':20},
                'level_19': {'type5':1, 'type8':5},
                'level_20': {'type6':1},
                'level_21': {'type1':1,'type2':1,'type3':1,'type4':1,'type5':1,'type6':1,'type7':1},
                'level_22': {'type7':10},
                'level_23': {'type5':20},
                'level_24': {'type3':30},
                }




def fair(x,y,speed):
        if y == 0:
                return speed,0
        rele = float(x/y)
        y = speed/float(rele + 1)
        x = y * rele 
        return x,y

class Gamemap(object):
        def __init__(self,size=(200,200), gameSize = (-2000,-2000,2000,2000), enemySize = 3, playerSize = 5):
                self.gameSize = gameSize
                self.playerSize = playerSize
                self.enemySize = enemySize
                self.size = size
                self.x1 = width - size[0]
                self.y1 = height - size[1]
                self.x2 = width
                self.y2 = height

        def realCoordsToMap(self,x,y):

                relation = (abs(self.gameSize[0]) + abs(self.gameSize[2])) / (self.size[0]) 
                x /= relation
                y /= relation

                x += self.x1
                y += self.y1
                return x+self.size[0]/2,y+self.size[1]/2

class Bullet(object):
        def __init__(self, x, y, direction, speed, framesToLive = 51, size = 10, friendly = True):
                self.size = size
                self.friendly = friendly
                self.friendlyActive = 0
                self.friendlyActiveBullets = 0
                self.bullets = []
                self.x = x
                self.y = y
                self.direction = direction
                self.speed = speed
                self.framesToLive = framesToLive
                self.age = 0 

        def collision(self):

                if self.friendly:
                        for i in xrange(len(enemies)):
                                if self.x + self.size / 2>= enemies[i].x1 and self.x - self.size / 2<= enemies[i].x2:
                                        if self.y + self.size / 2 >= enemies[i].y1 and self.y - self.size / 2 <= enemies[i].y2:
                                                bulletGod.friendlyActiveBullets -= 1
                                                if enemies[i].hp == 1:
                                                        del enemies[i]
                                                else:
                                                        enemies[i].hp -= 1
                                                return True

                else:
                        if self.x + self.size / 2 >= player.pos[0] and self.x - self.size / 2 <= player.pos[2]:
                                if self.y + self.size / 2 >= player.pos[1] and self.y - self.size / 2 <= player.pos[3]:
                                        if player.hp == 1:
                                                player.alive = False
                                        else:
                                                player.hp -= 1
                                        return True

                return False
                

        def updateBulletsAge(self):
                for i in xrange(len(self.bullets) - 1, -1, -1):
                        self.bullets[i].age += 1
                        if self.bullets[i].age > self.bullets[i].framesToLive:
                                if self.bullets[i].friendly:
                                        bulletGod.friendlyActiveBullets -= 1
                                del self.bullets[i]
                                



        def updateBulletsMovement(self):

                for bullet in self.bullets:
                        bullet.x += bullet.direction[0]
                        bullet.y += bullet.direction[1]
                        

        def makeBullets(self, speed = 15):

                direction = [0,0]
                for key in player.keyLog:
                        if key in [87,65,83,68]:

                                if key == 87:
                                        direction[1] -= speed
                                elif key == 83:
                                        direction[1] += speed
                                elif key == 65:
                                        direction[0] -= speed
                                else:
                                        direction[0] += speed

                if direction != [0,0]:

                        bulletGod.friendlyActiveBullets += 1
                        bullet = Bullet(400,400,direction,speed)
                        self.bullets.append(bullet)


                                
                                
class Player(object): # noen settings så spilleren starter med noe etterhvert ?
        def __init__(self, speed = 8, size = 50, hp=2,maxhp=3,maxAmmo=2, fakepos=[400,400]):
                self.hp = hp
                self.fakepos = [400,400]
                self.maxhp = maxhp
                self.maxAmmo = maxAmmo
                self.alive = True
                self.size = size
                self.timeStart = time.time()
                self.keyLog = []
                self.bullets = []
                self.speed = speed
                self.pos = [width/2 - size/2,
                                        height/2 - size/2,
                                        width/2 + size/2,
                                        height/2 + size/2]

        def restart(self,e):
                global enemies
                self.hp = 2
                self.maxhp = 3
                bulletGod.friendlyActiveBullets = 0
                self.alive = True
                self.timeStart = time.time()
                enemies = []
                bulletGod.bullets = []
                level['level'] = 0
                self.maxAmmo = 2

        def keyup(self, e):
                if e.keycode in self.keyLog:
                        self.keyLog.pop( self.keyLog.index(e.keycode) )

        def keydown(self, e):
                if not e.keycode in self.keyLog :
                        self.keyLog.append(e.keycode)


        def movement(self): # når player beveger seg så simulerer vi det med at alle de andre beveger seg motsatt vei

                if 37 in self.keyLog:
                        if self.fakepos[0] > -2000:
                                self.fakepos[0] -= self.speed
                                for enemy in enemies:
                                        enemy.x1 += self.speed
                                        enemy.x2 += self.speed
                                for bullet in bulletGod.bullets:
                                        bullet.x += self.speed

                if 38 in self.keyLog:
                        if self.fakepos[1] > - 2000:
                                self.fakepos[1] -= self.speed
                                for enemy in enemies:
                                        enemy.y1 += self.speed
                                        enemy.y2 += self.speed
                                for bullet in bulletGod.bullets:
                                        bullet.y += self.speed

                if 39 in self.keyLog:
                        if self.fakepos[0] < 2000:
                                self.fakepos[0] += self.speed
                                for enemy in enemies:
                                        enemy.x1 -= self.speed
                                        enemy.x2 -= self.speed
                                for bullet in bulletGod.bullets:
                                        bullet.x -= self.speed

                if 40 in self.keyLog:
                        if self.fakepos[1] < 2000:
                                self.fakepos[1] += self.speed
                                for enemy in enemies:
                                        enemy.y1 -= self.speed
                                        enemy.y2 -= self.speed
                                for bullet in bulletGod.bullets:
                                        bullet.y -= self.speed


class Enemy(object):
        def __init__(self, size = 20,
                     speed = 6,
                     hp = 1,
                     rangeAllowed=False,
                     rangeDelay=50,
                     rangeSize=5,
                     framesToLive = 1000,
                     rangeSpeed=5,
                     invisible = False,
                     invisibleDelay =50,
                     ):
                     

                self.invisible = invisible
                self.invisibleDelay = invisibleDelay
                self.invisibleTimer = 1
                self.visibleTimer = 0
                
                self.rangeSpeed = rangeSpeed
                self.framesToLive = framesToLive
                self.rangeAllowed = rangeAllowed
                self.rangeDelay = rangeDelay
                self.rangeDelayConstant = rangeDelay
                self.rangeSize = rangeSize
                self.hp = hp
                self.speed = speed
                self.size = size
                self.type = 1
                x1 = random.randint(-2000,0)
                y1 = random.randint(-2000,0)
                x2 = random.randint(1000,2000)
                y2 = random.randint(1000,2000)

                if abs(x1) + 1000 > x2:
                        x = x1
                else:
                        x = x2
                if abs(y1) + 1000 >= y2:
                        y = y1
                else:
                        y = y2

                self.x1 = x
                self.y1 = y
                self.x2 = x + self.size
                self.y2 = y + self.size
                self.fakePos = [self.x1,self.y1]

        def movement(self, rangeSpeed = 0):


                if self.invisible == True:
                        if self.invisibleTimer > 0:
                                self.invisibleTimer += 1
                        else:
                                self.visibleTimer += 1
                        if self.invisibleTimer == self.invisibleDelay:
                                self.invisibleTimer = 0
                                self.visibleTimer += 1
                        if self.visibleTimer == self.invisibleDelay:
                                self.visibleTimer = 0
                                self.invisibleTimer += 1
                        
                        
                        
                speed = self.speed

                if rangeSpeed > 0:
                        speed = rangeSpeed

                l1 = player.pos[0] + float(player.size/4) - self.x1 # player vil jo alltid stå samme sted...
                l2 = player.pos[1] + float(player.size/4) - self.y1 # kanskje lage bare et variabel for å la vær å regne det samme tallet om igjen
                # altså player.pos[0/1] + float(player.size/4)

                l3 = fair(abs(l1),abs(l2), speed)

                if l1 < 0:
                        l1 = - l3[0]
                else:
                        l1 = l3[0]
                if l2 < 0:
                        l2 = - l3[1]
                else:
                        l2 = l3[1]

                self.x1 += l1
                self.y1 += l2
                self.x2 = self.x1 + self.size
                self.y2 = self.y1 + self.size

                self.fakePos[0] += l1
                self.fakePos[1] += l2

                return l1,l2

        def hitPlayer(self):

                if self.x2 >= player.pos[0] and self.x1 <= player.pos[0] + player.size:
                        if self.y2 >= player.pos[1] and self.y1 <= player.pos[1] + player.size:
                                return True

        def shootPlayer(self):
                self.rangeDelay -= 1
                if self.rangeDelay == 0:
                        self.rangeDelay = self.rangeDelayConstant

                        vx,vy = self.movement(rangeSpeed = self.rangeSpeed)
                        direction = [vx,vy]

                        bullet = Bullet(self.x1+self.size/2,self.y1+self.size/2,direction,self.rangeSpeed,friendly = False,framesToLive = self.framesToLive)
                        bulletGod.bullets.append(bullet)
                        



class Application(Frame):


        def __init__(self, master):

                Frame.__init__(self, master)
                self.master.minsize(width=800, height=800)
                self.master.maxsize(width=800, height=800)
                self.master.bind("<KeyPress>", player.keydown)
                self.master.bind("<KeyRelease>", player.keyup)
                self.master.bind("r", player.restart)
                self.main_frame = Frame()
                self.main_frame.pack(fill='both', expand=True)
                self.c = Canvas(master, bg="white", width = 800, height = 800)
                self.c.pack(fill=BOTH, expand=YES)
                self.pack()

                self.animate()

        def animate(self):

                
                if player.alive:
                        self.c.delete("all")
                        self.c.create_rectangle(gamemap.x1,gamemap.y1,gamemap.x2,gamemap.y2)
                        px,py = gamemap.realCoordsToMap(player.fakepos[0],player.fakepos[1])
                        self.c.create_rectangle(px-gamemap.playerSize,
                                                py-gamemap.playerSize,
                                                px+gamemap.playerSize,
                                                py+gamemap.playerSize,
                                                fill="blue")
                        player.movement()

                        if len(enemies) == 0:
                                level['level'] += 1
                                player.fakepos = [400,400]
                                if level['level'] % 11 == 0:
                                        player.maxhp += 1
                                player.maxAmmo += 2
                                if player.hp < player.maxhp:
                                        player.hp += 1
                                for args in level['level_'+str(level['level'])]:
                                        for e in range(  level['level_'+str(level['level'])][args]  ) :
                                                if args == "type1":
                                                        enemies.append( Enemy(speed = 1) )
                                                elif args == "type2":
                                                        enemies.append( Enemy(size = 40,hp = 10) )
                                                elif args == "type3":
                                                        enemies.append( Enemy(size = 10, speed = 15) )
                                                elif args == "type4":
                                                        enemies.append( Enemy(size = 150, speed = 5, hp = 100) )
                                                elif args == "type5":
                                                        enemies.append( Enemy(size = 50, speed = 4, hp = 10, rangeAllowed = True,rangeSpeed = 5, framesToLive=250))
                                                elif args == "type6":
                                                        enemies.append( Enemy(size = 100, speed = 1, hp = 100, rangeAllowed = True,rangeSpeed = 30, framesToLive=300))
                                                elif args == "type7":
                                                        enemies.append( Enemy(size = 30,invisible = True))
                                                elif args == "type8":
                                                        enemies.append( Enemy(size = 50,invisible = True,
                                                                              hp = 30,
                                                                              speed = 0,
                                                                              rangeAllowed = True,
                                                                              rangeSpeed = 10,
                                                                              framesToLive=300,
                                                                              rangeDelay =10))

                        if bulletGod.friendlyActiveBullets < player.maxAmmo:
                                bulletGod.makeBullets()
                        else:
                                bulletGod.friendlyActiveBullets = player.maxAmmo
                        bulletGod.updateBulletsAge()
                        bulletGod.updateBulletsMovement()
                        

                        for i in xrange(len(bulletGod.bullets)-1,-1,-1):

                                self.c.create_oval(bulletGod.bullets[i].x , 
                                                                        bulletGod.bullets[i].y,
                                                                        bulletGod.bullets[i].x + bulletGod.bullets[i].size, 
                                                                        bulletGod.bullets[i].y + bulletGod.bullets[i].size)

                                if bulletGod.bullets[i].collision():
                                        del bulletGod.bullets[i]
                                        




                        for i in xrange(len(enemies)-1,-1,-1):

                                if enemies[i].invisible == False or enemies[i].visibleTimer == 0:
                                        self.c.create_rectangle(enemies[i].x1,
                                                                enemies[i].y1,
                                                                enemies[i].x2,
                                                                enemies[i].y2)
                                
                                enemies[i].movement()
                                mapx,mapy = gamemap.realCoordsToMap(enemies[i].fakePos[0] +enemies[i].size/2,
                                                                    enemies[i].fakePos[1] +enemies[i].size/2)

                                self.c.create_oval(mapx-gamemap.enemySize,
                                                   mapy-gamemap.enemySize,
                                                   mapx+gamemap.enemySize,
                                                   mapy+gamemap.enemySize,
                                                   fill="red")
                                
                                if enemies[i].rangeAllowed:
                                        enemies[i].shootPlayer()
                                if enemies[i].hitPlayer():
                                        player.hp -= 1
                                        enemies[i].hp -= 5
                                        if player.hp == 0:
                                                player.alive = False
                                        else:
                                                if enemies[i].hp <= 0:
                                                        del enemies[i]
                                        
                        self.c.create_rectangle(player.pos)

                else:
                        self.c.create_text(400,250,text ="RIP, press r to restart", font=("Courier",20))
                        self.c.create_text(400,300,text ="You survived to level " + str(level['level']), font=("Courier",20))
                        # la oss lage en egen level dict som kan si hvor mange av hvilken klasse som skal komme på hver level
                        # kanskje lag en type fiende der det er forhåndsbestemt hvor den skal spawne!

                self.c.create_text(100,50,text ="Level: " + str(level['level']), font=("Courier",15))
                self.c.create_text(700,50,text =str(time.time()-player.timeStart).split(".")[0] + " seconds", font=("Courier",15))
                self.c.create_text(100,730,text ="Bullets: " + str(bulletGod.friendlyActiveBullets) + "/"+str(player.maxAmmo), font=("Courier",15))
                self.c.create_text(400,50,text ="Health: " + str(player.hp), font=("Courier",15))
                self.c.create_text(700,580,text = str(player.fakepos), font=("Courier",20))

                self.c.after(20, self.animate)


#####bulletGod.friendlyActiveBullets
player = Player()
gamemap = Gamemap()
bulletGod = Bullet(0,0,1,1)
root = Tk()
app = Application(root)
app.mainloop()
