import paho.mqtt.client as mqtt
import threading
import json
import time

# MQTT broker information
broker_address = "broker.example.com"
port = 1883

# MQTT topics
proposal_topic = "paxos/proposal"
promise_topic = "paxos/promise"
accept_topic = "paxos/accept"
decision_topic = "paxos/decision"

# Shared data structures
proposals = {}  # Proposal ID -> (offer, proposal_num, ranking)
accepts = {}  # Proposal ID -> (offer, proposal_num, accept_count, total_ranking)

# List of offers
offers = [
    {"id": 1, "product": "T-shirt", "price": 20, "discount": "20% off"},
    {"id": 2, "product": "Shoes", "price": 50, "discount": "Buy one, get one free"},
    {"id": 3, "product": "Watch", "price": 100, "discount": "30% off"},
    {"id": 4, "product": "Headphones", "price": 80, "discount": "Limited-time discount"},
    {"id": 5, "product": "Backpack", "price": 40, "discount": "Free shipping"},
    {"id": 6, "product": "Sunglasses", "price": 30, "discount": "Buy one, get one 50% off"},
    {"id": 7, "product": "Jeans", "price": 60, "discount": "20% off"},
    {"id": 8, "product": "Jacket", "price": 90, "discount": "Special price for today only"},
    {"id": 9, "product": "Dress", "price": 70, "discount": "Buy 2, get 1 free"},
    {"id": 10, "product": "Smartphone", "price": 500, "discount": "Free accessory with purchase"}
]

# Paxos node
class PaxosNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.proposal_num = 0
        self.offer = None

    def prepare(self, proposal_id):
        self.proposal_num = max(self.proposal_num, proposal_id) + 1
        return self.proposal_num, self.offer

    def promise(self, proposal_id, last_proposal_num, last_offer, last_ranking):
        if proposal_id not in accepts:
            accepts[proposal_id] = {"offer": last_offer, "proposal_num": last_proposal_num, "accept_count": 0, "total_ranking": last_ranking}
            return True, self.offer
        else:
            return False, None

    def accept(self, proposal_id, offer, ranking):
        accepts[proposal_id]["accept_count"] += 1
        accepts[proposal_id]["total_ranking"] += ranking
        return True

    def decide(self):
        majority_proposal = max(accepts.items(), key=lambda x: (x[1]["accept_count"], x[1]["total_ranking"]))[0]
        self.offer = accepts[majority_proposal]["offer"]
        return self.offer

# MQTT client
class MQTTClient:
    def __init__(self, client_id):
        self.client_id = client_id

    def on_connect(self, client, userdata, flags, rc):
        print(f"{self.client_id}: Connected with result code {rc}")
        client.subscribe([promise_topic, accept_topic, decision_topic])

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = json.loads(msg.payload)
        if topic == promise_topic:
            self.handle_promise(payload)
        elif topic == accept_topic:
            self.handle_accept(payload)
        elif topic == decision_topic:
            self.handle_decision(payload)

    def send_message(self, topic, payload):
        client.publish(topic, json.dumps(payload))

    def handle_promise(self, promise):
        proposal_id = promise["proposal_id"]
        last_proposal_num = promise["last_proposal_num"]
        last_offer = promise["last_offer"]
        last_ranking = promise["last_ranking"]
        success, offer = node.promise(proposal_id, last_proposal_num, last_offer, last_ranking)
        if success:
            self.send_message(accept_topic, {"proposal_id": proposal_id, "offer": offer})

    def handle_accept(self, accept):
        proposal_id = accept["proposal_id"]
        offer = accept["offer"]
        ranking = accept["ranking"]
        success = node.accept(proposal_id, offer, ranking)
        if success:
            print(f"{self.client_id}: Accepted offer: {offer}")

    def handle_decision(self, decision):
        offer = decision["offer"]
        print(f"{self.client_id}: Consensus reached! Offer: {offer}")

# Create MQTT client instance
client = mqtt.Client()

# Connect to MQTT broker
client.connect(broker_address, port)

# Instantiate Paxos node
node = PaxosNode("Node-1")

# Instantiate MQTT clients
clients = [MQTTClient(f"Client-{i}") for i in range(50)]

# Set MQTT client callbacks
for client_instance in clients:
    client_instance.client.on_connect = client_instance.on_connect
    client_instance.client.on_message = client_instance.on_message

# Start MQTT client loop in separate threads
client.loop_start()
threads = []
for client_instance in clients:
    thread = threading.Thread(target=client_instance.client.loop_forever)
    threads.append(thread)
    thread.start()

# Simulate proposal with ranking
proposal_id = 1
for i in range(50):
    ranking = (i % 5) + 1  # Each client ranks the offer from 1 to 5
    clients[i].send_message(proposal_topic, {"proposal_id": proposal_id, "offer": offers[i % len(offers)], "ranking": ranking})

# Wait for threads to finish
for thread in threads:
    thread.join()

# Disconnect MQTT client
client.disconnect()
