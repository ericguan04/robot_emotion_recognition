#!/usr/bin/env python3

'''
Facial Expression + Robot Movement Research
General emotion movement script
'''

import rospy
from geometry_msgs.msg import Twist

running = True

# Function to stop robot
def stopRobot(event):
    global running
    running = False

def autonomousMovement(name, time, linear_vel, angular_vel):
    global running
    rospy.init_node(name)
    rate = rospy.Rate(10) #10 Hz

    # Initialize a publisher to send velocity commands
    # Publish to /cmd_vel_mux/input/navi topic to send Twist movement to stage_sim
    cmd_vel_pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=10)

    # Create a Twist message to publish velocity commands
    move_cmd = Twist()
    move_cmd.linear.x = linear_vel # Move forward at 'linear_vel' m/s
    move_cmd.angular.z = angular_vel # Rotate at 'angular_vel' m/s

    # Run the robot for 'time' seconds
    duration = rospy.Duration.from_sec(time)

    # Start a timer to stop the robot after the specified duration
    rospy.Timer(duration, stopRobot)

    while running and not rospy.is_shutdown():
        cmd_vel_pub.publish(move_cmd)
        rospy.loginfo(str(move_cmd.linear.x) + " " + str(move_cmd.angular.z)) # Telemetry data
        rate.sleep()

    # Stop the robot after the specified duration
    move_cmd.linear.x = 0.0 # Stop
    cmd_vel_pub.publish(move_cmd)
    running = True