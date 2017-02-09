#!/usr/bin/env python
print("hello")
import sys
print(sys.version)
import rospy
from chat_server.msg import Message

new_messages = list()


def callback(data):
    new_messages.append((data.sender, data.message))


def run_server():
    global new_messages
    pub = rospy.Publisher('chat_out', Message, queue_size=10)
    rospy.init_node('chat_server', anonymous=True)
    rospy.Subscriber('chat_in', Message, callback)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        messages = new_messages
        new_messages = list()
        for message in messages:
            pub.publish(sender=message.sender, message=message.message)
        rate.sleep()

if __name__ == "__main__":
    try:
        run_server()
    except rospy.ROSInterruptException:
        pass
