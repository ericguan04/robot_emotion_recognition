#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

turning = False

# Function to stop robot
def stop_turning(event):
    global turning
    turning = False

def sensor_test():
    global turning
    rospy.init_node('turtlebot_sensor_test')
    rate = rospy.Rate(10) #10 Hz

    # Initialize a publisher to send velocity commands
    cmd_vel_pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=10)
    # Initialize a subscriber to to receive sensor data
    scan_sub = rospy.Subscriber('/scan', LaserScan, queue_size=10)

    # Create a Twist message to publish velocity commands
    move_cmd = Twist()
    move_cmd.linear.x = 0.2
    move_cmd.angular.z = 0.0

    while not rospy.is_shutdown():
        global turning        
        # Receive messages from subscriber
        scan_msg = rospy.wait_for_message('/scan', LaserScan)
        
        # Range in front of robot
        mid_index = int(len(scan_msg.ranges) / 2)
        range_in_front = scan_msg.ranges[mid_index]

        if range_in_front < 1.0:
            duration = rospy.Duration.from_sec(1.0)
            rospy.Timer(duration, stop_turning)
            turning = True

            while turning:
                move_cmd.linear.x = 0.01
                move_cmd.angular.z = -1.50
                cmd_vel_pub.publish(move_cmd)
                rospy.loginfo('turning')
        else:
            move_cmd.linear.x = 0.2
            move_cmd.angular.z = 0.0
            rospy.loginfo(range_in_front)
            cmd_vel_pub.publish(move_cmd)

        rate.sleep()

    # Stop the robot after the specified duration
    move_cmd.linear.x = 0.0 # Stop
    cmd_vel_pub.publish(move_cmd)
    rospy.loginfo('End of program')


if __name__ == '__main__':
    try:
        sensor_test()
    except rospy.ROSInterruptException:
        pass