# # import paho.mqtt.client as mqtt
# # import time
# # import random
# # from threading import Thread

# # # MQTT broker details
# # broker_address = "localhost"
# # broker_port = 1883

# # # Offer topic
# # offer_topic = "offer"

# # # Paxos variables
# # proposals = {}  # Dictionary to store proposals
# # ratings = {}    # Dictionary to store ratings for accepted proposals
# # max_proposal_id = 0
# # max_accepted_id = 0
# # accepted_value = None

# # # Create a MQTT client instance
# # client = mqtt.Client()

# # # Callback function when a message is received
# # def on_message(client, userdata, message):
# #     global max_proposal_id, max_accepted_id, accepted_value

# #     # Simulate receiving an offer message
# #     received_offer = str(message.payload.decode("utf-8"))

# #     # Paxos logic
# #     proposal_id = max_proposal_id + 1
# #     if proposal_id not in proposals:
# #         # If the proposal is new, accept it and send an accept message
# #         proposals[proposal_id] = received_offer
# #         if proposal_id > max_proposal_id:
# #             max_proposal_id = proposal_id
# #             # Simulate sending an accept message
# #             accepted_value = received_offer
# #             max_accepted_id = proposal_id
# #             send_accept_message(proposal_id, received_offer)
# #     else:
# #         # If the proposal already exists, check if it's been accepted
# #         if proposal_id > max_accepted_id:
# #             # If the proposal hasn't been accepted, accept it and send an accept message
# #             max_accepted_id = proposal_id
# #             accepted_value = received_offer
# #             send_accept_message(proposal_id, received_offer)

# # # Function to send an accept message
# # def send_accept_message(proposal_id, value):
# #     # Simulate sending the accept message via MQTT
# #     accept_message = f"{proposal_id}:{value}"
# #     client.publish("paxos/accept", accept_message)
# #     print("Accept message sent:", accept_message)

# # # Connect to the broker
# # client.connect(broker_address, broker_port)

# # # Subscribe to the offer topic
# # client.subscribe(offer_topic)

# # # Set callback function for message reception
# # client.on_message = on_message

# # # Start the MQTT loop in a separate thread
# # client.loop_start()

# # # Function to rate the offer
# # def rate_offer(offer):
# #     # Simulate rating the offer
# #     rating = random.randint(1, 5)  # Random rating between 1 and 5
# #     print("Offer received:", offer)
# #     print("Please rate the offer (1-5):", rating)
# #     return rating

# # # Function to send feedback
# # def send_feedback(offer, rating):
# #     # Simulate sending feedback message via MQTT
# #     feedback_message = f"Offer: {offer}, Rating: {rating}"
# #     client.publish("offer/feedback", feedback_message)
# #     print("Feedback sent:", feedback_message)

# # # Function to process received offers and rate them
# # def process_offer(offer):
# #     rating = rate_offer(offer)
# #     send_feedback(offer, rating)

# # # Start the MQTT loop
# # while True:
# #     # Simulate continuous processing of received offers
# #     time.sleep(5)  # Wait for offers to be received

# import paho.mqtt.client as mqtt
# import time
# import random
# from threading import Thread

# # MQTT broker details
# broker_address = "localhost"
# broker_port = 1883

# # Offer topic
# offer_topic = "offer"

# # Paxos variables
# proposals = {}  # Dictionary to store proposals
# ratings = {}    # Dictionary to store ratings for accepted proposals
# max_proposal_id = 0
# max_accepted_id = 0
# accepted_value = None

# # Create a MQTT client instance
# client = mqtt.Client()

# # Callback function when a message is received
# def on_message(client, userdata, message):
#     global max_proposal_id, max_accepted_id, accepted_value

#     # Simulate receiving an offer message
#     received_offer = str(message.payload.decode("utf-8"))

#     # Paxos logic
#     proposal_id = max_proposal_id + 1
#     if proposal_id not in proposals:
#         # If the proposal is new, accept it and send an accept message
#         proposals[proposal_id] = received_offer
#         if proposal_id > max_proposal_id:
#             max_proposal_id = proposal_id
#             # Simulate sending an accept message
#             accepted_value = received_offer
#             max_accepted_id = proposal_id
#             send_accept_message(proposal_id, received_offer)
#     else:
#         # If the proposal already exists, check if it's been accepted
#         if proposal_id > max_accepted_id:
#             # If the proposal hasn't been accepted, accept it and send an accept message
#             max_accepted_id = proposal_id
#             accepted_value = received_offer
#             send_accept_message(proposal_id, received_offer)

# # Function to send an accept message
# def send_accept_message(proposal_id, value):
#     # Simulate sending the accept message via MQTT
#     accept_message = f"{proposal_id}:{value}"
#     client.publish("paxos/accept", accept_message)
#     print("Accept message sent:", accept_message)

# # Connect to the broker
# client.connect(broker_address, broker_port)

# # Subscribe to the offer topic
# client.subscribe(offer_topic)

# # Set callback function for message reception
# client.on_message = on_message

# # Start the MQTT loop in a separate thread
# client.loop_start()

# # Function to rate the offer
# def rate_offer(offer):
#     # Simulate rating the offer
#     rating = random.randint(1, 5)  # Random rating between 1 and 5
#     print("Offer received:", offer)
#     print("Please rate the offer (1-5):", rating)
#     return rating

# # Function to send feedback
# def send_feedback(offer, rating):
#     # Simulate sending feedback message via MQTT
#     feedback_message = f"Offer: {offer}, Rating: {rating}"
#     client.publish("offer/feedback", feedback_message)
#     print("Feedback sent:", feedback_message)

# # Function to process received offers and rate them
# def process_offer(offer):
#     rating = rate_offer(offer)
#     send_feedback(offer, rating)

# # Start the MQTT loop
# while True:
#     # Simulate continuous processing of received offers
#     time.sleep(5)  # Wait for offers to be received

import paho.mqtt.client as mqtt
import time
import random

# MQTT broker details
broker_address = "localhost"
broker_port = 1883

# Offer topic
offer_topic = "offers"

# Paxos variables
proposals = {}  # Dictionary to store proposals
ratings = {}    # Dictionary to store ratings for accepted proposals
max_proposal_id = 0
max_accepted_id = 0
accepted_value = None

# Create a MQTT client instance
client = mqtt.Client()

# Callback function when a message is received
def on_message(client, userdata, message):
    global max_proposal_id, max_accepted_id, accepted_value

    # Decode the received message
    proposal_id, received_offer = str(message.payload.decode("utf-8")).split(':')
    proposal_id = int(proposal_id)

    # Paxos logic to accept the proposal
    if proposal_id > max_proposal_id:
        max_proposal_id = proposal_id
        proposals[proposal_id] = received_offer
        if proposal_id > max_accepted_id:
            max_accepted_id = proposal_id
            accepted_value = received_offer
            send_accept_message(proposal_id, received_offer)

# Function to send an accept message
def send_accept_message(proposal_id, value):
    accept_message = f"{proposal_id}:{value}"
    client.publish("paxos/accept", accept_message)
    print("Accept message sent:", accept_message)

# Connect to the broker
client.connect(broker_address, broker_port)

# Subscribe to the offer topic
client.subscribe(offer_topic)

# Set the callback function for message reception
client.on_message = on_message

# Start the MQTT loop in a separate thread
client.loop_start()

# Function to rate the offer
def rate_offer(offer):
    rating = random.randint(1, 5)
    print("Offer received:", offer)
    print("Please rate the offer (1-5):", rating)
    return rating

# Function to send feedback
def send_feedback(offer, rating):
    feedback_message = f"Offer: {offer}, Rating: {rating}"
    client.publish("offer/feedback", feedback_message)
    print("Feedback sent:", feedback_message)

# Main loop to continuously process received offers
while True:
    # Check if there's an accepted offer to rate
    if accepted_value:
        rating = rate_offer(accepted_value)
        send_feedback(accepted_value, rating)
        accepted_value = None
    time.sleep(5)
