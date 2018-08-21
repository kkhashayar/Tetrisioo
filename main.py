'''
Simple implementation of The classic game Tetris.
by Khashayar Nariman   19/Aug/2018
Using python3
turtle module for graphics!
pygame.mixer for sound
'''

import turtle, random, os, time, copy, pygame
from collections import Counter 
pygame.mixer.init()

# all the sound files 
count_sound = pygame.mixer.Sound("count.ogg")
welcome_music = pygame.mixer.Sound("start.wav")
back_ground_music = pygame.mixer.Sound("Tetris.ogg")
block_sound = pygame.mixer.Sound("penclick1.wav")
rotate_sound = pygame.mixer.Sound("rotate_block.wav")
clean_line = pygame.mixer.Sound("clean.wav")
#-- Constants
distance = 20
row = 30
col = 15

#-- setting up the screen 
screen = turtle.Screen()
screen.setup(700,700,700)
screen.bgcolor("black")
screen.tracer(False) 

# Setting the fonts for on screen display 
font = ("arial", "18", "bold")
font2 = ("arial","18")
font3 = ("arial", "80", "bold")

# welcome screen, using separate function, calling the turtle module only once 
# and have separate control on it, by this way we can clear the screen much 
# easier 
def welcome():
    p = turtle.Turtle()
    p.penup()
    p.hideturtle()
    p.setpos(-150,100)
    p.pencolor("yellow")
    welcome_music.play()
    p.write("welcome to tetrisioo!", font = font)
    time.sleep(1)
    p.setpos(-150, 70)
    welcome_music.play()
    p.write("by Khashayar, Nariman", font = font)
    p.pencolor("white")
    time.sleep(1)
    p.setpos(-150, 30)
    count_sound.play()
    p.write("Up to rotate",font = font2)
    time.sleep(0.50)
    p.setpos(-150, 10)
    count_sound.play()
    p.write("Down to drop",font = font2)
    time.sleep(0.50)
    p.setpos(-150, -10)
    count_sound.play()
    p.write("Left to left",font = font2)
    time.sleep(0.50)
    p.setpos(-150, -30)
    count_sound.play()
    p.write("Right to right",font = font2)
    time.sleep(3)
    p.clear()
    p.setpos(-200,100)
    p.write("Ready?!", font = font3)
    time.sleep(2)
    p.clear()
    p.setpos(0,0)
    p.pencolor("orange")
    p.write("3", font = font3)
    time.sleep(1)
    p.clear()
    p.pencolor("gold")
    p.write("2", font = font3)
    time.sleep(1)
    p.clear()
    p.pencolor("yellow")
    p.write("1", font = font3)
    time.sleep(1)
    p.clear()
    p.pencolor("red")
    p.write("Go!", font = font3)
    time.sleep(1)
    p.clear()
welcome_music.play()
welcome()
# stand alone function to draw the graphical board, 
# the board is just for display, doesnt have any functionality
def draw_board():
    p = turtle.Turtle()
    p.speed(0)
    p.hideturtle()
    p.penup()
    p.setpos(-310,310)
    p.shape("square")
    p.shapesize(1)
    p.pencolor("green")
    p.fillcolor("black")
    for r in range(row):
        for c in range(col):
            screen.update()
            p.stamp()
            p.forward(distance)
        p.back(distance * col)
        p.right(90)
        p.forward(distance)
        p.left(90)
    p.setpos(-320,320)
    for i in range(4):
        p.pensize(4)
        p.color("green")
        p.pendown()
        p.forward(distance * col)
        p.right(90)
        p.forward(distance * row)
        p.right(90)
#--------------------------
# Class shape holds the attributes of shapes, using 0,1 to form the blocks
# each shape represented as a 2D array 
class Shape(turtle.Turtle):
    def __init__(self):
        #-- Graphic attribs 
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.penup()
        self.speed(0)
        self.setpos(-310, 310)
        self.shape("square")
        self.shapesize(0.9)
        self.pencolor("green")
        self.fillcolor("black")
        #-- Game attribs
        self.on_board = "off"
        self.dropping = "off"
        self.next_shape = "on"
        self.base = [[0,0,0,0]]
        self.temp_shape = self.base
        self.current_shape = self.base
        self.next_spot = 0
        self.next_contact = 0
        self.next_stamp = 0
        self.last_stamp = 0
        self.bottom = 0
        self.x_move = 0
        self.y_move = 0
        self.default_time = 200 # tick
        self.tick = self.default_time
        self.temp_positions = []
        self.up_coming_shape = self.base
        self.o  = [[0,1,1,0],
                   [0,1,1,0]]
        self.l_1 =[[0,1,0,0],
                   [0,1,0,0],
                   [0,1,0,0],
                   [0,1,1,0]]
        self.l_2 =[[1,1,1,1],
                   [1,0,0,0]]
        self.l_3 =[[0,1,1,0],
                   [0,0,1,0],
                   [0,0,1,0],
                   [0,0,1,0]]
        self.l_4 =[[0,0,0,1],
                   [1,1,1,1]]
        self.t_1 =[[0,1,1,1],
                   [0,0,1,0]]
        self.t_2 =[[0,0,1,0],
                   [0,1,1,0],
                   [0,0,1,0]]
        self.t_3 =[[0,0,1,0],
                   [0,1,1,1]]
        self.t_4 =[[0,0,1,0],
                   [0,0,1,1],
                   [0,0,1,0]]
        self.s_1 =[[0,0,1,1],
                   [0,1,1,0]]
        self.s_2 =[[0,1,0,0],
                   [0,1,1,0],
                   [0,0,1,0]]
        self.s_3 =[[0,1,1,0],
                   [0,0,1,1]]
        self.s_4 =[[0,0,1,0],
                   [0,1,1,0],
                   [0,1,0,0]]
        self.i_1 =[[0,0,1,0],
                   [0,0,1,0],
                   [0,0,1,0],
                   [0,0,1,0]]
        self.i_2 =[[1,1,1,1]]
      
        self.all_shapes = [self.o , self.s_1, self.s_2, self.s_3,
                                 self.s_4, self.t_1, self.t_2, self.t_3,
                                 self.t_4, self.l_1, self.l_2, self.l_3,
                                 self.l_4, self.i_1, self.i_2]

        self.l = [self.l_1, self.l_2, self.l_3, self.l_4]
        self.s = [self.s_1, self.s_2, self.s_3, self.s_4]
        self.t = [self.t_1, self.t_2, self.t_3, self.t_4]
        self.i = [self.i_1, self.i_2]
        self.height = len(self.current_shape)
        self.width  = len(self.current_shape[0])
        self.first_shape = "on"
    
    # Draw method will display shapes on the board in each time frame 
    # isntead of drawing i used stamp() method, 
    def draw(self):
        if len(self.temp_positions) != 0:
            self.temp_positions.clear()
            
        if self.next_shape == "on":
            self.on_board = "off"
            if self.first_shape == "on":#-- one time switch for the first move
                self.current_shape = random.choice(self.all_shapes)#-- one time direct choice from all_shapes 
                self.first_shape = "off"
            else:
                self.current_shape = self.up_coming_shape
            self.fillcolor("light green")
            self.next_shape = "off"
            self.on_board = "on"
            #-- This is the next block, and we use it for preview in separate function
            self.up_coming_shape = random.choice(self.all_shapes)
        #-- Check if items in shape lists are 1 or 0.
        for r in range(len(self.current_shape)):
            for c in range(len(self.current_shape[0])):
                
                if self.current_shape[r][c] == 1:
                    self.shapesize(0.9)
                    self.fillcolor("gold")
                    self.bottom = self.ycor()
                    self.next_stamp = self.pos()
                    if self.xcor() <= -310:
                        self.setx(-310)
                    elif self.xcor() >= -30:
                        self.setx(-30)
                    self.temp_positions.append(self.pos())
                else:
                    self.shapesize(1)
                    self.fillcolor("black")
                self.stamp()
                self.forward(distance)
            self.back(distance * self.width)
            self.right(90)
            self.forward(distance)
            self.left(90)
        self.last_stamp = self.temp_positions[-1]
        screen.update()

    # Checking the evnts..
    def get_next_spot(self):
        if self.x_move == 0:
            return(self.xcor(), (self.ycor()-distance))
        if self.x_move != 0:
            return (self.xcor() + self.x_move,self.ycor())
            self.x_move = 0
            return self.x_move
    # Check for next available spot to drop
    def update(self):
        self.setheading(0)
        self.next_spot = self.get_next_spot()
        self.next_contact = (self.xcor(), (self.ycor()-distance * 2))
        if self.x_move == 0: 
            if self.dropping is "off":
                self.dropping = "on"

            if self.dropping is "on":
                self.draw()
                self.goto(self.next_spot)
                self.dropping = "off"
        else:
            self.dropping = "off"
            if self.dropping is "off":
                self.goto(self.next_spot)
                self.goto(self.xcor(), self.ycor() + 20)
                self.draw()
                self.x_move = 0
    # using internal turtle rotator to rotate the current shape 
    def rotate(self):
        rotate_sound.play()
        self.dropping = "off"
        if self.current_shape in self.l:
            try:
                self.r = self.l.index(self.current_shape)
                if self.r == len(self.l):
                    self.r = 0
                    self.current_shape = self.l[self.r]
                    
                else:
                    self.current_shape = self.l[self.r +1]
            except IndexError:
                self.r = 0
                self.current_shape = self.l[self.r]
        #-- clear rotation 
        elif self.current_shape in self.s:
            try:
                self.r = self.s.index(self.current_shape)
                if self.r == len(self.s):
                    self.r = 0
                    self.current_shape = self.s[self.r]
                else:
                    self.current_shape = self.s[self.r + 1]
            except IndexError:
                self.r = 0
                self.current_shape = self.s[self.r]
        elif self.current_shape in self.t:
            try:
                self.r = self.t.index(self.current_shape)
                if self.r == len(self.t):
                    self.r = 0
                    self.current_shape = self.s[self.r]
                else:
                    self.current_shape = self.t[self.r + 1]
            except IndexError:
                self.r = 0
                self.current_shape = self.t[self.r]
        elif self.current_shape in self.i:
            try:
                self.r = self.i.index(self.current_shape)
                if self.r == len(self.i):
                    self.r = 0
                    self.current_shape = self.i[self.r]
                else:
                    self.current_shape = self.i[self.r + 1]
            except IndexError:
                self.r = 0
                self.current_shape = self.i[self.r]
        return True 
    # using keybinding listen() function for event handling 
    def move_left(self):
        self.dropping = "off"
        self.x_move -= 20
        return self.x_move 
        
    def move_right(self):
        self.dropping = "off"
        self.x_move += 20
        return self.x_move

    def move_down(self):
        self.tick = 5
# Class game keep attributes of the Game, clean, clone and keep a track of all blocks and their coordinates 
# on the board
class Game(turtle.Turtle):
    def __init__(self, shape):
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.penup()
        self.pencolor("black")
        self.fillcolor("white")
        self.shape("square")
        self.shapesize(0.9)
        self.g_board = []
        self.setpos(-310,310)
        #-- for game update, check and rebuild the board
        self.point = 0 
        self.temp_board = []
        self.data_board = {}
        self.keys = []
        self.rebuild = "off"
        self.xcors = [-310, -290, -270, -250, -230,
                      -210, -190, -170, -150, -130,
                      -110, -90, -70, -50, -30]
        self.ycors = [310, 290, 270, 250, 230, 210,
                      190, 170, 150, 130, 110, 90,
                      70, 50, 30, 10, -10, -30, -50,
                     -70, -90, -110, -130, -150, -170,
                     -190, -210, -230, -250, -270,]
        self.rows = []
        self.all_keys = []
        self.rows = []
        self.row_counter = 0
        self.r = None
#-----------------------------------------------------------------------------------------
    # i thought of using dictionary to keep a track of position and coordinations of available blocks on the board
    # but later on i came up with easier way, but i just left the method for the record.
    def build_data_board(self):
        for x in self.xcors:
            for y in self.ycors:
                self.data_board.update({(x,y): 0})
#-----------------------------------------------------------------------------------------
    
    # Counts the number of the blocks in each row using counter() function from collections module
    def check(self):
        try:
            for item, number in self.row_counter.items():
                if number == 15:
                    self.r = item
                    self.clean_board()
        except RuntimeError:
            pass
        
    def clean_board(self):
        # i used different patterns and this one worked the way i expected
        # slowing the update screen a bit to having an animated style while cleaning the lines 
        # i used stamp() function to clean the blocks 
        # remove them from the board
        # give the rest of the blocks new coordination
        # clone the board using deep copy 
        # rebuild the board by new positions 
        
        screen.tracer(2)
        self.fillcolor("black")
        count_g_board = 0
        count_rows = 0 
        #print("in clean_board method!")
        #print("clening the g board")
        #time.sleep(0.001)
        for i in self.g_board:
            if i[1] == self.r:
                self.goto(i)
                self.stamp()
                self.g_board.remove(i)
                # here i kept missing elements using loop, for example there was 8 blocks to clean,
                # but every time code missed 1 or 2 of them
                # maybe i had to use map to avoid the problem!
                count_g_board += 1
                #print("count_g_board:", count_g_board)
                #time.sleep(0.001)
            if count_g_board != 15:
                #print("second attemp to clean the line!")
                #time.sleep(0.001)
                for i in self.g_board:
                    if i[1] == self.r:
                        self.goto(i)
                        self.stamp()
                        self.g_board.remove(i)
                        count_g_board += 1
                        #print("count_g_board:", count_g_board)
                        #time.sleep(0.001)
                
        for i in self.rows:
            if i == self.r:
                self.rows.remove(i)
                count_rows += 1
                #print("count rows: ", count_rows)
                #time.sleep(0.001)
            if count_rows != 15:
                #print("second attemp to clean the rows!")
                #time.sleep(0.001)
                for i in self.rows:
                    if i == self.r:
                        self.rows.remove(i)
                        count_rows += 1
                        #print("count rows: ", count_rows)
                        #time.sleep(0.001)
        screen.tracer(0)
        self.clone_board()
    # Used counters to be sure the operation is done without any mistake
    def clone_board(self):
        #os.system("clear")
        #print("in clone-board methid !")
        #time.sleep(0.20)
        count1= 0
        count2 = 0
        count3 = 0
        count4 = 0 
        temp = []
        for position in self.g_board:
            if position[1] > self.r:
                self.goto(position)
                self.stamp()
                temp.append(self.pos())
                count1 += 1
                #print("copy to temp: ", count1)
                #time.sleep(0.001)
        for position in temp:
            if position in self.g_board:
                self.g_board.remove(position)
                count2 += 1
                #print(" removed from g-board: ", count2)
                #time.sleep(0.001)
        if count2 != count1:
            #print("error syncing between temp and g board!.. trying again")
            self.clone_board()
        else:
            pass

        self.fillcolor("gold")
        for position in temp:
            if position[1] > self.r:
                position -= (0.0, 20.0)
                count3 +=1
                #print(count3)
                self.goto(position)
                self.stamp()
                screen.update()
                self.g_board.append(self.pos())
                count4 += 1
        self.rows.clear()

        for position in self.g_board:
            self.goto(position)
            self.rows.append(self.ycor())
        if len(self.g_board) != len(self.rows):
            for position in self.g_board:
                self.goto(position)
                self.rows.append(self.ycor())
        clean_line.play()
        self.point += 10
        if self.point == 50:
            shape.default_time -= 50
        point()
        
                
    def update(self):
        self.row_counter = Counter(self.rows)
        #-- Runtime status 
        #os.system("clear")
        count = 0 
        #if self.r != None:
        #    print("self.r: ",self.r)
        #else:
        #    print("self.r: ", 0)
        #print("row counter: ",self.row_counter)
        #print("len of self.rows: ",len(self.rows))
        #print("len g_board: ", len(self.g_board))
        #-------------------------------------------------------
        for position in shape.temp_positions:
            position -= (0.0,20.0)
            if position in self.g_board or shape.bottom <= -270:
                shape.tick = shape.default_time
                block_sound.play()
                self.fillcolor("gold")
                self.pencolor("black")
                if self.rebuild is "off":
                    for position in shape.temp_positions:
                        if position not in self.g_board:
                            self.goto(position)
                            self.stamp()
                            self.g_board.append(self.pos())
                            #-- I can add ycors to self.rows for keep tracking of rows
                            self.rows.append(self.ycor())
                            shape.next_shape = "on"
                            shape.setpos(random.randrange(-310,-90, distance), 310)
                        else:
                            pass
                else:
                    pass
        self.check()

#--------------------- Creating objects, connecting the shape and game class
draw_board()
shape = Shape()
game = Game(shape)
#game.build_data_board()

# Separate function to display score
def point():
    colors = ["yellow", "white","orange","lightblue","lightgreen"]
    p = turtle.Turtle()
    p.shape("square")
    p.shapesize(3)
    p.penup()
    p.hideturtle()
    p.pencolor("black")
    p.fillcolor("black")
    p.setpos(100,0)
    p.stamp()
    p.pencolor(random.choice(colors))
    p.write(game.point, font = font)
    

p1 = turtle.Turtle()
font = ("Arial", "20")
p2 = turtle.Turtle()
p2.hideturtle()
p2.penup()
p2.setpos(100,230)
p2.pencolor("white")
p2.write("Next", font = font)
p2.setpos(100,40)
p2.write("score", font = font)

# display next upcoming shape
# a reason to write it with separate function, out of the class was cleaning the screen after each update 
# if we use it as method inside a class with clean() function turtle would erase the whole graphics inherited from
# That class
def preview():
    #time.sleep(1)
    p1.hideturtle()
    p1.penup()
    p1.setpos(100,200)
    p1.shape("square")
    p1.shapesize(1)
    p1.fillcolor("lightblue")
    for r in range(len(shape.up_coming_shape)):
        for c in range(len(shape.up_coming_shape[0])):
            if shape.up_coming_shape[r][c] == 1:
                p1.stamp()
                p1.forward(distance)
            else:
                p1.forward(distance)
        p1.back(distance * shape.width)
        p1.right(90)
        p1.forward(distance)
        p1.left(90)
        
#--- Key bindings and event handling 
turtle.listen()
turtle.onkey(shape.move_left,"Left")
turtle.onkey(shape.move_right,"Right")
turtle.onkey(shape.move_down,"Down")
turtle.onkey(shape.rotate,"Up")

# Main function, contains the main game loop! 
def main():
    running = True
    back_ground_music.set_volume(0.1)#-- looping the music 
    back_ground_music.play(-1)#-- volume control 
    while running:
        preview() # Display the next upcoming shape
        #-- Instead of using time module its much better to use builtin ontimer() function 
        turtle.ontimer(game.update(), t= shape.tick)
        turtle.ontimer(shape.update(),t= shape.tick)
        #-- update the screen depending on screen.tracer() builtin function
        screen.update()
        shape.clear()
        p1.clear()

if __name__ == "__main__":
    main()
    
