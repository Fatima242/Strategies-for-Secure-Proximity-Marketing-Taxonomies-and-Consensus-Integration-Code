import paho.mqtt.client as mqtt
import threading
import json
import time
import random

# MQTT broker information
broker_address = "broker.example.com"
port = 1883

# MQTT topics
proposal_topic = "raft/proposal"
response_topic = "raft/response"

# Shared data structures
proposals = {}  # Proposal ID -> (offer, proposal_num)
accepted_proposal = None  # Proposal accepted by the majority

# List of offers
offers = [
    {"id": 1, "product": "T-shirt", "price": 20, "discount": "20% off"},
    {"id": 2, "product": "Shoes", "price": 50, "discount": "Buy one, get one free"},
    {"id": 3, "product": "Watch", "price": 100, "discount": "30% off"},
    {"id": 4, "product": "Headphones", "price": 80, "discount": "Limited-time discount"},
    {"id": 5, "product": "Backpack", "price": 40, "discount": "Free shipping"},
    {"id": 6, "product": "Sunglasses", "price": 30, "discount": "50% off"},
    {"id": 7, "product": "Jeans", "price": 60, "discount": "20% off"},
    {"id": 8, "product": "Jacket", "price": 90, "discount": "Special price for today only"},
    {"id": 9, "product": "Dress", "price": 70, "discount": "Buy 2, get 1 free"},
    {"id": 10, "product": "Smartphone", "price": 500, "discount": "Free accessory with purchase"}
]

# Raft node
class RaftNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.leader = None

    def handle_proposal(self, proposal_id, offer):
        # Simulate Raft's leader election and consensus algorithm
        if self.leader == self.node_id:
            # Only leader processes the proposal
            if proposal_id not in proposals:
                proposals[proposal_id] = offer
                self.broadcast_response(proposal_id, offer)

    def broadcast_response(self, proposal_id, offer):
        # Simulate broadcasting the response to all nodes
        global accepted_proposal
        # Simulate acceptance by majority of nodes
        if random.random() > 0.5:  # Simulating majority acceptance
            accepted_proposal = (proposal_id, offer)
            # Publish the accepted proposal as a response
            payload = {"proposal_id": proposal_id, "offer": offer}
            client.publish(response_topic, json.dumps(payload))

# MQTT client
class MQTTClient:
    def __init__(self, client_id):
        self.client_id = client_id

    def on_connect(self, client, userdata, flags, rc):
        print(f"{self.client_id}: Connected with result code {rc}")
        client.subscribe(proposal_topic)
        client.subscribe(response_topic)  # Subscribe to the response topic as well

    def on_message(self, client, userdata, msg):
        if msg.topic == proposal_topic:
            payload = json.loads(msg.payload)
            proposal_id = payload["proposal_id"]
            offer = payload["offer"]
            raft_node.handle_proposal(proposal_id, offer)
        elif msg.topic == response_topic:
            # Handle response messages if needed
            pass

    def send_proposal(self, proposal_id, offer):
        payload = {"proposal_id": proposal_id, "offer": offer}
        client.publish(proposal_topic, json.dumps(payload))

# Create MQTT client instance
client = mqtt.Client()

# Connect to MQTT broker
client.connect(broker_address, port)

# Instantiate Raft node
raft_node = RaftNode("Node-1")

# Instantiate MQTT client
mqtt_client = MQTTClient("Client")

# Set MQTT client callbacks
client.on_connect = mqtt_client.on_connect
client.on_message = mqtt_client.on_message

# Start MQTT client loop
client.loop_start()

# Simulate proposal
proposal_id = 1
for offer in offers:
    mqtt_client.send_proposal(proposal_id, offer)
    proposal_id += 1

# Simulate waiting for 1 minute for clients to rate the offers
time.sleep(60)  # 1 minute delay

# Print accepted proposal
if accepted_proposal:
    print("Consensus reached! Accepted proposal:", accepted_proposal)
else:
    print("Consensus not reached.")

# Disconnect MQTT client
client.disconnect()
