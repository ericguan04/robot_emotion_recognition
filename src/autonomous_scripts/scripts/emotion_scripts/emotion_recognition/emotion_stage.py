'''
Calls the timedCameraRecognition method to get dominant emotion
Uses dominant emotion and autonomousMovement method to run scripts
'''

from timed_camera_recogntion import timedCameraRecognition
from autonomous_movement import autonomousMovement
import rospy

emotion = timedCameraRecognition(15, False)

if emotion == "happy":
    try:
        #move forward
        autonomousMovement('happy_script', 5, 0.2, 0)

        rospy.loginfo('happy script completed')
        rospy.loginfo('moved forward for 5 seconds at 0.2 m/s')
    except rospy.ROSInterruptException:
        pass
    
elif emotion == "angry":
    try:
        #turn left
        autonomousMovement('angry_script', 4, 0, 0.41)
        
        #move forward
        autonomousMovement('angry_script', 5, 0.2, 0)

        rospy.loginfo('angry script completed')
        rospy.loginfo('moved left for 5 seconds at 0.2 m/s')
    except rospy.ROSInterruptException:
        pass

elif emotion == "sad":
    try:
        #turn right
        autonomousMovement('sad_script', 4, 0, -0.41)
        
        #move forward
        autonomousMovement('sad_script', 5, 0.2, 0)

        rospy.loginfo('sad script completed')
        rospy.loginfo('moved right for 5 seconds at 0.2 m/s')
    except rospy.ROSInterruptException:
        pass

elif emotion == "surprise":
    try:
        #move backwards
        autonomousMovement('surprise_script', 5, -0.2, 0)

        rospy.loginfo('surprise script completed')
        rospy.loginfo('moved backwards for 5 seconds at 0.2 m/s')
    except rospy.ROSInterruptException:
        pass