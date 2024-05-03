#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

running = True

# Function to stop robot
def stop_robot(event):
    global running
    running = False

def autonomous_movement():
    global running
    rospy.init_node('stage_autonomous_movement')
    rate = rospy.Rate(10) #10 Hz

    # Initialize a publisher to send velocity commands
    # Publish to /cmd_vel_mux/input/navi topic to send Twist movement to stage_sim
    cmd_vel_pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=10)

    # Create a Twist message to publish velocity commands
    move_cmd = Twist()
    move_cmd.linear.x = 0.2 # Move forward at 0.2 m/s
    move_cmd.angular.z = 0.0 # No rotation

    # Run the robot for 5 seconds
    duration = rospy.Duration.from_sec(2.0)

    # Start a timer to stop the robot after the specified duration
    rospy.Timer(duration, stop_robot)

    while running and not rospy.is_shutdown():
        cmd_vel_pub.publish(move_cmd)
        rospy.loginfo(move_cmd.linear.x) # Telemetry data
        rate.sleep()

    # Stop the robot after the specified duration
    move_cmd.linear.x = 0.0 # Stop
    cmd_vel_pub.publish(move_cmd)
    rospy.loginfo('End of program')


if __name__ == '__main__':
    try:
        autonomous_movement()
    except rospy.ROSInterruptException:
        pass