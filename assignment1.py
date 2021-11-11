from __future__ import print_function

import time
from sr.robot import *

##
# \file assignment1.py
# \brief This file contains one possible solution to the first RT1 assignment
# \author Emanuele Rambaldi
# \version 0.1
# \date 5/11/2021
#
# \details This assignment aim is to guide the robot shown in the simulation through the established path, grabbing the silver tokens that it ecounters and moving them behind it and avoiding 
# collision with golden tokens.


# \details Run with: $ python2 run.py assignment1.py


##
# \details float: Threshold for the control of the angular displacement between the robot and a silver token: it defines the maximum angular displacement for grabbing a silver token 
a_th = 2.0

##
# \details float: Threshold for the control of the linear distance between the robot and a silver token: it defines the maximum distance for grabbing a silver token
d_th = 0.4

##
# \details float: Linear threshold for defining an area of detection in order to avoid collision with golden tokens
dan_th = 0.9

##
# \details float: Angular threshold for defining an area of detection in order to avoid collision with golden tokens
per_dan_th = 40

##
# \details float: Linear threshold for defining an area in which it is checked the number of golden blocks in order to properly change the direction of the robot
near_th = 1.6

##
# \details float: Angular threshold for defining an area in which it is checked the number of golden blocks in order to properly change the direction of the robot
per_near_th = 135

##
# \details float: Angular threshold for defining an area in which it is checked the distance from the nearest golden block in order to properly change the direction of the robot
per_wall_th1= 75

##
# \details float: Angular threshold for defining an area in which it is checked the distance from the nearest golden block in order to properly change the direction of the robot
per_wall_th2= 105

##
# \details float: Linear threshold for defining an area of detection of silver tokens
sil_th = 1.2

##
# \details float: Angular threshold for defining an area of detection of silver tokens
per_sil_th = 90

##
# \details instance of the class Robot 
R = Robot()


##
# \brief Function for setting a linear velocity.
# \param Speed: the speed of the two wheels of the robot (int)
# \param Seconds: the time interval after which the wheels stop turning (int)
# \return No return values

def drive(speed, seconds):

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

##
# \brief Function for setting an angular velocity.
# \param Speed: the the speed of the two wheels of the robot (int)
# \param Seconds: the time interval after which the wheels stop turning (int)
# \return No return values
#
# \details Differently from the "drive" function, here a wheel i set at speed, whereas the other is set at -speed. This is a way to impose an angular velocity to the robot.

def turn(speed, seconds):

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

##
# \brief Function to check if there are any golden tokens within a certain distance (dan_th) in a certain angular range (from -per_dan_th to per__dan_th).
# \param No parameters
# \return Number of golden tokens found in the scanned area (int)
#
# \details The list of all the tokens around the robot is returned by the method R.see() of the class Robot. From that list the check is run.


def check_dangerous_tokens():
    n_dangers = 0
    tokens = R.see()
    for i in range(0, len(tokens)):
        if ((tokens[i].info.marker_type == "gold-token")and(tokens[i].dist <= dan_th)and(-per_dan_th <= tokens[i].rot_y <= per_dan_th)):
            n_dangers = n_dangers+1
    return n_dangers

##
# \brief Function to count the number of golden tokens on the left and on the right of the robot within a certain distance (near_th) in a certain angular range (from -per_near_th to per_near_th).
# \param No parameters
# \return Number of golden tokens on the left in the scanned area (int)
# \return Number of golden tokens on the right in the scanned area (int)
#
# \details The list of all the tokens around the robot is returned by the method R.see() of the class Robot. From that list the check is run.

def count_tokens():

    n_left_tokens=0
    n_right_tokens=0
    tokens = R.see()
    for i in range(0, len(tokens)):
        if((tokens[i].info.marker_type == "gold-token")and(tokens[i].dist <= near_th)and(-per_near_th <= tokens[i].rot_y <= per_near_th)):
            if (tokens[i].rot_y<=0):
                    n_left_tokens = n_left_tokens+1
                    print("left token:", tokens[i])
            else:
                    n_right_tokens = n_right_tokens+1
                    print("right token:", tokens[i])
    print(n_left_tokens, n_right_tokens)
    return n_left_tokens, n_right_tokens

##
# \brief Function to change the direction of the robot according to: 
# - the number of golden tokens on the left and the number of golden tokens on the right passed as input
# - the distance form the nearest golden wall in a certain angular range (from -per_wall_th2 to -per_wall_th1 and from per_wall_th1 to per_wall_th2)
# \param Number of golden tokens on the left of the robot (int)
# \param Number of golden tokens on the right of the robot (int)
# \return No return value
#
# \details The list of all the tokens around the robot is returned by the method R.see() of the class Robot. From that list the check is run.

def change_direction(n_left_tokens, n_right_tokens):

    min_dist_wall=100
    if (n_left_tokens >  n_right_tokens):
        turn(+20, 0.1)
    elif (n_left_tokens < n_right_tokens):
        turn(-20, 0.1)
    elif (n_left_tokens == n_right_tokens):
        tokens = R.see()
        for i in range(0, len(tokens)):
            if ((tokens[i].info.marker_type == "gold-token")and((-per_wall_th2 <= tokens[i].rot_y <= -per_wall_th1)or(per_wall_th1 <= tokens[i].rot_y <= per_wall_th2))):
                if(tokens[i].dist <= min_dist_wall):
                    min_dist_wall=tokens[i].dist
                    rot_min_dist_wall=tokens[i].rot_y
        print("wall at minimum distance:", min_dist_wall)
        print("angular displacement wall at minimum distance:", rot_min_dist_wall)
        if(rot_min_dist_wall<=0):
            turn(+20, 0.5)
        else:
            turn(-20, 0.5)

##
# \brief Function to detect if there are any silver tokens within a certain distance (sil_th) in a certain angular range (from -per_sil_th to per_sil_th).
# \param No parameters
# \return Distance of the detected silver token from the robot (float) or -1
# \return Angular displacement between the detected silver token and the robot (float) or -1
#
# \details The list of all the tokens around the robot is returned by the method R.see() of the class Robot. From that list the check is run.

def detect_silver_tokens():
    dist = 100
    tokens = R.see()
    for i in range(0, len(tokens)):
        if ((tokens[i].info.marker_type == "silver-token")and(tokens[i].dist <= sil_th)and(-per_sil_th <= tokens[i].rot_y <= per_sil_th)):
            dist=tokens[i].dist
            ang_disp=tokens[i].rot_y
    if (dist == 100):
        return -1, -1
    else:
        return dist, ang_disp




##
# \brief Function that calls all the other ones.
# \param No parameters
# \return No return values
#
# \details By calling the other functions, the main function guide the robot along the path defined by the golden blocks in counter-clockwise direction, making sure that it does not collide with them. 
# Furthermore it makes the robot detect the silver blocks that it encounters along the way, makes it grab them and move them behind itself.

def main():
    while(1):
        drive(100, 0.16)
        dist, ang_disp = detect_silver_tokens()
        if (dist != -1):
            print("Found a silver token pal")
            if (dist >= d_th):
                while((ang_disp < -a_th)or(ang_disp > a_th)):
                    if (ang_disp < -a_th):
                        print("Left a bit...")
                        turn(-4, 0.25)
                    elif (ang_disp > a_th):
                        print("Right a bit...")
                        turn(+4,0.25)
                    dist, ang_disp = detect_silver_tokens()
            else:
                if(R.grab()):
                    print("Gotcha!")
                    heading = R.heading
                    print(heading)
                    if(heading>=0):
                        heading_minus_three=heading-3
                        while(heading>heading_minus_three):
                            turn(-40,0.05)
                            heading = R.heading
                    else:
                        heading_plus_three=heading+3
                        while(heading<heading_plus_three):
                            turn(40,0.05)
                            heading = R.heading
                    R.release()
                    drive(-20,0.9)
                    heading = R.heading
                    print(heading)
                    if(heading>=0):
                        heading_minus_three=heading-3
                        while(heading>heading_minus_three):
                            turn(-40,0.05)
                            heading = R.heading
                    else:
                        heading_plus_three=heading+3
                        while(heading<heading_plus_three):
                            turn(40,0.05)
                            heading = R.heading
        else:
            n_dangers = check_dangerous_tokens()
            if (n_dangers!=0):
                print("Attention! Dangerous tokens detected")
                while(n_dangers!=0):
                    n_left_tokens, n_right_tokens = count_tokens()
                    change_direction(n_left_tokens, n_right_tokens)
                    n_dangers=check_dangerous_tokens()
                           
            
main()