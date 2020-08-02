import turtle
import os
import winsound
import math
import random
import platform

#If on Windows,you import winsound, or better yet, just use Linux
if platform.system() == "Windows":
    try:
        import winsound
    except:
        print("Windsound module not available.")

#Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.setup(700,700)
wn.title("Space Invaders")
wn.bgpic("space_invaders_background1.gif")
wn.tracer(0)

#Register the shapes
 
#Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

#Set the score to 0
score = 0

#Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290,280)
scorestring = "Score: {}".format(score)
score_pen.write(scorestring, False, align="left", font=("Arial",14,"normal"))
score_pen.hideturtle()

#Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("triangle")
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)
player.speed = 0

#Choose a number of enemies
number_of_enemies = 30
#Create an empty list of enemies
enemies = []

#Add enemies to the list
for i in range(number_of_enemies):
    #Create the enemy
    enemies.append(turtle.Turtle())

enemy_start_x = -225
enemy_start_y = 250
enemy_number = 0

for enemy in enemies:
    enemy.color("red")
    enemy.shape("circle")
    enemy.penup()
    enemy.speed(0)
    x = enemy_start_x + (50 * enemy_number)
    y = enemy_start_y 
    enemy.setposition(x,y)
    #Update the enemy number
    enemy_number += 1
    if enemy_number == 10:
        enemy_start_y -= 50
        enemy_number = 0

enemyspeed = 0.2

#Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle()

bulletspeed = 7

#Define bullet state
#ready - ready to fire
#fire - bullet is firing
bulletstate = "ready"

#Move the player left and right
def move_left():
    player.speed = -3
    
def move_right():
    player.speed = 3
    x= player.xcor()
    x += player.speed
    player.setx(x)

def move_player():
    x= player.xcor()
    x += player.speed
    if x < -280:
       x = -280
    if x > 280:
       x = 280
    player.setx(x)

def fire_bullet():
    #Declare bulletstate as a global if it needs changed
    global bulletstate
    if bulletstate == "ready":
      winsound.PlaySound("laser.wav", winsound.SND_ASYNC)
      bulletstate = "fire"
      #Move the bullet to the just above the player
      x = player.xcor()
      y = player.ycor() + 10
      bullet.setposition(x,y)
      bullet.showturtle()

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 15:
        return True
    else:
        return False

def play_sound(sound_file, time = 0):
    #Windows
    if platform.system == "Windows":
        winsound.PlaySound(sound_file, winsound.SND_ASYNC)
    #Linux
    elif platform.system == "Linux":
        os.system("aplay -q {}&".format(sound_file))
    #Mac
    else:
        os.system("afplay {}&".format(sound_file))

    #Repeat sound
    if time > 0:
        turtle.ontimer(lambda: play_sound(sound_file, time), t=int(time * 1000))
#Create keyboard bindings
wn.listen()
wn.onkeypress(move_left,"Left")
wn.onkeypress(move_right,"Right")
wn.onkeypress(fire_bullet,"space")

#Main game loop
while True:
   wn.update()
   move_player()

   for enemy in enemies:
     #Move the enemy
     x = enemy.xcor()
     x += enemyspeed
     enemy.setx(x)

     #Move the enemy back and down
     if enemy.xcor() > 280:
        #Move all the enemies down
        for e in enemies:
          y = e.ycor()
          y -= 40
          e.sety(y)
        #Change enemy direction
        enemyspeed *= -1

     if enemy.xcor() < -280:
        #Move all the enemies down
        for e in enemies:
          y = e.ycor()
          y -= 40
          e.sety(y)
        #Change enemy direction
        enemyspeed *= -1

     #Check for a collision between the bullet and the enemy
     if isCollision(bullet, enemy):
         winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
         #Reset the bullet
         bullet.hideturtle()
         bulletstate = "ready"
         bullet.setposition(0,-400)
         #Rsest the enemy
         enemy.setposition(0,10000)
         #Update the score
         score += 10
         scorestring = "Score: {}".format(score)
         score_pen.clear()
         score_pen.write(scorestring, False, align="left", font=("Arial",14,"normal"))
    
     if isCollision(player, enemy):
         winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
         player.hideturtle()
         enemy.hideturtle()
         print("Game Over")
         break

  #Move the bullet
   if bulletstate == "fire":
    y = bullet.ycor()
    y += bulletspeed
    bullet.sety(y)
 
  #Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
     bullet.hideturtle()
     bulletstate = "ready"


delay = input("Press Enter")