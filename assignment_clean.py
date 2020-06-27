#!/usr/bin/env python3
# license removed for brevity
import rospy
import time
import math
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

turtlesim_pose = Pose()

def move_straight(speed,distance,is_forward):
	vel_msg = Twist()

	if(is_forward == 'y' or is_forward == 'Y'):
		vel_msg.linear.x = abs(speed)
	else:
		vel_msg.linear.x = -abs(speed)

	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0

	t0 = rospy.Time.now().to_sec()
	current_distance = 0.0
	loop_rate = rospy.Rate(10)

	while(current_distance<distance):
		velocity_pub.publish(vel_msg)
		t1 = rospy.Time.now().to_sec()
		current_distance = speed * (t1-t0)
		loop_rate.sleep()

	vel_msg.linear.x = 0;
	velocity_pub.publish(vel_msg)

def tut_rotation(angular_speed, d_angle, clockwise):
	vel_msg = Twist()

	if (clockwise == 'y' or clockwise == 'Y'):
		vel_msg.angular.z = -abs(angular_speed)
	else:
		vel_msg.angular.z = abs(angular_speed)
	
	vel_msg.linear.x = 0
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0

	t0 = rospy.Time.now().to_sec()
	current_angle = 0.0
	loop_rate = rospy.Rate(10)

	while(current_angle<d_angle):
		velocity_pub.publish(vel_msg)
		t1 = rospy.Time.now().to_sec()
		current_angle = angular_speed * (t1-t0)
		loop_rate.sleep()
	
	vel_msg.angular.z = 0;
	velocity_pub.publish(vel_msg)

def absolute_angle (des_angle):
	relative_angle = des_angle - turtlesim_pose.theta
	if(relative_angle>0):
		clockwise = 'n'
	else: clockwise = 'y'
	tut_rotation(abs(relative_angle)/4, abs(relative_angle),clockwise)


def move_goal(x_goal,y_goal):
	velo_msg = Twist()
	velo_msg.linear.y = 0
	velo_msg.linear.z = 0
	velo_msg.angular.x =0
	velo_msg.angular.y = 0

	while(True):
		eucli_dist = math.sqrt((x_goal - turtlesim_pose.x)**2 + (y_goal - turtlesim_pose.y)**2)
		angular_velo = math.atan2(y_goal-turtlesim_pose.y,x_goal - turtlesim_pose.x)

		velo_msg.linear.x = 1 * eucli_dist
		velo_msg.angular.z = 4 * (angular_velo - turtlesim_pose.theta)
		velocity_pub.publish(velo_msg)

		if(eucli_dist<0.01):
			break
	
	velo_msg.linear.x = 0
	velo_msg.angular.z = 0
	velocity_pub.publish(velo_msg)

	print("\nX co-ordinates",turtlesim_pose.x,"\nY co-ordinates",turtlesim_pose.y)

def grid_clean():
	forward = 'y'
	start_x = 1.0
	start_y = 1.0
	loop_rate = rospy.Rate(10)
	move_goal(start_x,start_y)
	loop_rate.sleep()

	absolute_angle(0)
	loop_rate.sleep()

	move_straight(2,9, forward)
	loop_rate.sleep()
	clockwise = 'n'
	tut_rotation(deg2rad(10),deg2rad(90),clockwise)
	loop_rate.sleep()

	move_straight(2,9, forward)
	tut_rotation(deg2rad(10),deg2rad(90),clockwise)
	loop_rate.sleep()

	move_straight(2,1, forward)
	tut_rotation(deg2rad(10),deg2rad(90),clockwise)
	loop_rate.sleep()

	move_straight(2,9, forward)
	clockwise = 'y'
	tut_rotation(deg2rad(10),deg2rad(90),clockwise)
	loop_rate.sleep()

	move_straight(2,1, forward)
	tut_rotation(deg2rad(10),deg2rad(90),clockwise)
	loop_rate.sleep()

	move_straight(2,9, forward)

def sprial_cleaning():
	veloc_msg = Twist()
	costant_speed = 4.0
	rk = 0.5
	loop_rate = rospy.Rate(10)
	while(True):
		rk = rk + 0.1
		veloc_msg.linear.x = rk
		veloc_msg.linear.y = 0
		veloc_msg.linear.z = 0
		veloc_msg.angular.x = 0
		veloc_msg.angular.y = 0
		veloc_msg.angular.z = costant_speed

		velocity_pub.publish(veloc_msg)
		print("linear velocity: ",veloc_msg.linear.x,"\nAngular velocity: ", veloc_msg.angular.z)
		
		if ((turtlesim_pose.x > 10.5) or  (turtlesim_pose.y > 10.5)):
			break
		loop_rate.sleep()

	veloc_msg.linear.x = 0
	velocity_pub.publish(veloc_msg)

########################################################################
def pose_topic_sub_callback(pose_data):

	turtlesim_pose.x = pose_data.x
	turtlesim_pose.y = pose_data.y
	turtlesim_pose.theta = pose_data.theta

def deg2rad(value):
	return value*(pi/180)



if __name__ == '__main__':

	pi = 3.14159265359
	rospy.init_node("straight_movement", anonymous = True)
	velocity_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
	rospy.Subscriber("/turtle1/pose", Pose, pose_topic_sub_callback)

	menu = int(input("\nEnter 1 for spiral cleaning and 2 for grid cleaning : "))

	if (menu == 1):
		sprial_cleaning()
	elif (menu == 2):
		grid_clean()
	else:
		print("\n##### ERROR ----> ENTER VALID INPUT #####\n")
