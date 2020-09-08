from sense_hat import SenseHat
from time import sleep

# Object constructions.

sense = SenseHat()

# End object constructions.


# Configurations.

shutdown = False
sleep_time = 0.25

bat_y = 4;
ball_position = [3, 3]
ball_velocity = [1, 1]
score = 0

white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

# End configurations.


# Functions.

def draw_bat():
    if (shutdown == True):
        return
    
    sense.set_pixel(0, bat_y, red)
    sense.set_pixel(0, bat_y + 1, red)
    sense.set_pixel(0, bat_y - 1, red)

def draw_ball():
    if (shutdown == True):
        return
    
    global bat_y
    global ball_position
    global ball_velocity
    global score
    
    sense.set_pixel(ball_position[0], ball_position[1], blue)
    
    # Move the ball on the x as.
    ball_position[0] += ball_velocity[0]
    if ball_position[0] == 7 or ball_position[0] == 0:
        ball_velocity[0] = -ball_velocity[0]

    # Move the ball on the y as.
    ball_position[1] += ball_velocity[1]
    if ball_position[1] == 7 or ball_position[1] == 0:
        ball_velocity[1] = -ball_velocity[1]

    # Bounce the ball back if we hit the bat
    if ball_position[0] == 1 and (bat_y - 1) <= ball_position[1] <= (bat_y + 1):
        ball_velocity[0] = -ball_velocity[0]
        score += 1
    
    if ball_position[0] == 0:
        sense.show_message("Score: %s You lose" % score)
        
        bat_y = 4;
        ball_position = [3, 3]
        ball_velocity = [1, 1]

def move_up(event):
    global bat_y
    if event.action == 'pressed' and bat_y > 1:
        bat_y -= 1

def move_down(event):
    global bat_y
    if event.action == 'pressed' and bat_y < 6:
        bat_y += 1

def reset(event):
    global bat_y
    global ball_position
    global ball_velocity
    global score
    
    if event.action == 'pressed':
        bat_y = 4;
        ball_position = [3, 3]
        ball_velocity = [1, 1]
        score = 0

def shutdown(event):
    global shutdown
    
    if event.action == 'pressed':
        if (shutdown == False):
            shutdown = True
        else:
            shutdown = False
            
        reset(event)

# End functions.


# Main program.

sense.stick.direction_up = move_up
sense.stick.direction_down = move_down
sense.stick.direction_left = reset
sense.stick.direction_right = shutdown

while True:
    sense.clear(0,0,0)
    
    draw_bat()
    draw_ball()
    
    sleep(sleep_time)

# End program.
