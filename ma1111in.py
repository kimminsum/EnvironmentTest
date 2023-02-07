print("Booting Up...")
import time
import math
import random
import turtle
turtle.colormode(255)


# some changable variables
FPS = 60
REPROENERGY = 80 # the energy needed to reproduce
OFFENERGY = 50 # 50% of energy given to the offspring
WINDOWSIZE = [600,600]
ENTITYFIELD = [500,500]
STARTCOUNT = [10,10]
ENERGYPERTICK = 0.5
EVOLUTIONMULT = [1,1,1]


class groupA():
    def __init__(self,size,speed,sense,xy):
        #traits
        self.siz = size
        self.spd = speed
        self.sen = sense
        if xy == "random":
            self.xy = [random.randint(WINDOWSIZE[0]/2-ENTITYFIELD[0]/2, ENTITYFIELD[0]/2+WINDOWSIZE[0]/2), random.randint(ENTITYFIELD[1]/2-WINDOWSIZE[1]/2, ENTITYFIELD[1]/2+WINDOWSIZE[1]/2)]
        else:
            self.xy = xy
        self.enr = REPROENERGY*OFFENERGY/100
        self.rot = random.randint(0, 360)

class groupB():
    def __init__(self,size,speed,sense):
        self.siz = size
        self.spd = speed
        self.sen = sense



#initializing turtles
wn = turtle.Screen() ; wn.title("") ; wn.bgcolor("white") ; wn.setup(width=WINDOWSIZE[0],height=WINDOWSIZE[1]) ; wn.tracer(0)
fpsText = turtle.Turtle();fpsText.penup();fpsText.pencolor("Black");fpsText.pensize(3);fpsText.speed(0);fpsText.goto(WINDOWSIZE[0]/2-50,WINDOWSIZE[1]/2-40);fpsText.ht()
entityPen = turtle.Turtle();entityPen.penup();entityPen.pencolor("Black");entityPen.pensize(3);entityPen.speed(0);entityPen.goto(0,0);entityPen.ht()


groupA_A = []
for i in range(5):
    #size speed sense
    groupA_A.append(groupA(random.randrange(20,50,1),4,10,"random"))

def drawEntity(xy,size,color):
    global entityPen
    entityPen.pencolor(color)
    entityPen.pensize(size)
    entityPen.goto(xy[0]-300,xy[1]-300);entityPen.pendown()
    entityPen.goto(entityPen.xcor(),entityPen.ycor());entityPen.penup()


def renderEntities():
    global groupA_A,entityPen
    entityPen.clear()
    
    for groupA in groupA_A:
        drawEntity(groupA.xy,groupA.siz,(0,math.floor(groupA.enr/100*255),0))

def calculateEntities():
    global groupA_A,WINDOWSIZE,ENTITYFIELD,ENERGYPERTICK,REPROENERGY,EVOLUTIONMULT,groupA
    offSpring = []
    
    for entity in groupA_A:
        xy = [entity.xy[0] + math.cos(math.pi/180*entity.rot)*entity.spd , entity.xy[1] + math.sin(math.pi/180*entity.rot)*entity.spd]
        
        # Gaining energy
        entity.enr += ENERGYPERTICK*entity.siz/50
        if entity.enr > 100:
            entity.enr = 100
        
        #Reproducing
        if entity.enr > REPROENERGY:
            offSpring.append([entity.siz + random.randrange(EVOLUTIONMULT[0]*-10,EVOLUTIONMULT[0]*10,1)/10,entity.spd + random.randrange(EVOLUTIONMULT[1]*-10,EVOLUTIONMULT[1]*10,1)/10,entity.sen + random.randrange(EVOLUTIONMULT[1]*-10,EVOLUTIONMULT[1]*10,1)/10,entity.xy])
            entity.enr *= (100-OFFENERGY)/100
            #entity.enr = math.floor(entity.enr)
        
        #Wall collision
        for i in range(2):
            if xy[i] < (WINDOWSIZE[i]/2-ENTITYFIELD[i]/2):
                xy[i] = WINDOWSIZE[i]-ENTITYFIELD[i]-xy[i]
            elif xy[i] > WINDOWSIZE[i]/2+ENTITYFIELD[i]/2:
                xy[i] = WINDOWSIZE[i]+ENTITYFIELD[i]-xy[i]
            else:
                continue

            if not i :
                entity.rot -= 180
            entity.rot *=-1
            entity.rot %= 360
        
        entity.xy = xy
    for i in range(len(offSpring)):
        groupA_A.append(groupA(offSpring[i][0],offSpring[i][1],offSpring[i][2],offSpring[i][3]))


fpsTime = time.perf_counter()
actFps,fpsCount = 0, 0
def fpsCheck():
    global fpsTime,actFps,fpsCount
    fpsCount +=1
    if fpsCount >= 10:
        #actual fps
        actFps = math.floor(10/(time.perf_counter()-fpsTime))
        fpsTime = time.perf_counter()
        fpsCount = 0
    fpsText.clear()
    fpsText.write(f"FPS : {actFps}",align="center",font=("Courier",10,"bold"))
    return fpsCount



while True:
    calculateEntities()
    renderEntities()
    
    fpsCheck()
    wn.update()
    time.sleep(1/FPS)

