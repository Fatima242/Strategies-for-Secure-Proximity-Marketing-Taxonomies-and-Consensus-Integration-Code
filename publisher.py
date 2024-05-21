import paho.mqtt.client as mqtt
import time
import random

# MQTT broker details
broker_address = "localhost"
broker_port = 1883

# Offer topic
offer_topic = "offer"

# List of offers
offers = [
    "T-shirt offer: 20% off",
    "Shoe offer: Buy one, get one free",
    "Accessory offer: Free shipping on all accessories",
    "Electronics offer: Limited-time discounts on electronics",
    "Food offer: Special deals on selected food items"
]

# Create a MQTT client instance
client = mqtt.Client()

# Connect to the broker
client.connect(broker_address, broker_port)

# Function to send an offer
def send_offer():
    while True:
        # Select a random offer from the list
        selected_offer = random.choice(offers)
        
        # Publish the selected offer to the offer topic
        client.publish(offer_topic, selected_offer)
        print("Offer published:", selected_offer)

        time.sleep(5)  # Simulate some interval between offers

# Start sending offers in a separate thread
offer_thread = Thread(target=send_offer)
offer_thread.start()

# Start the MQTT loop
client.loop_forever()
