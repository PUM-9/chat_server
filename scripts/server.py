#!/usr/bin/env python
import rospy
from chat_server.msg import Message
from chat_server.srv import *

new_messages = list()
pub = None


def callback(data):
    new_messages.append((data.sender, data.message))


def get_nmbr_of_clients(req):
    global pub
    return NmbClientsResponse(pub.get_num_connections())


def run_server():
    global new_messages
    global pub
    pub = rospy.Publisher('chat_out', Message, queue_size=10)
    rospy.init_node('chat_server', anonymous=False)
    rospy.Subscriber('chat_in', Message, callback)
    s = rospy.Service('nmb_of_clients', NmbClients, get_nmbr_of_clients)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        messages = new_messages
        new_messages = list()
        for message in messages:
            pub.publish(sender=message[0], message=message[1])
        rate.sleep()

if __name__ == "__main__":
    try:
        run_server()
    except rospy.ROSInterruptException:
        pass
