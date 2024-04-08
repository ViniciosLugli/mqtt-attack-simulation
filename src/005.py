import unittest
from common import MQTTClient
import threading
import time


class MQTTIntegrityTest(unittest.TestCase):
    broker_address = "localhost"
    port = 1891
    topic = "integrity/topic"

    def on_message(self, client, userdata, msg):
        # Assume legitimate messages should start with 'Legit:'
        if msg.payload.decode().startswith("Legit:"):
            self.legitimate_messages_received += 1
        else:
            self.unauthorized_messages_received += 1

    def setUp(self):
        self.legitimate_messages_received = 0
        self.unauthorized_messages_received = 0
        # Setup a legitimate client that listens for messages on the topic
        self.legitimate_client = MQTTClient("legitimate_client", self.broker_address, self.port, override_on_message=self.on_message)
        self.legitimate_client.connect()
        self.legitimate_client.subscribe(self.topic, qos=0)
        time.sleep(1)  # Wait for subscription to complete

    def tearDown(self):
        self.legitimate_client.disconnect()

    def test_unauthorized_message_integrity_violation(self):
        # Simulate an attacker sending a message that doesn't follow the expected format
        attacker_client = MQTTClient("attacker_client", self.broker_address, self.port)
        attacker_client.connect()
        attacker_client.publish(self.topic, "Fake: This is not a legitimate message", qos=0)
        attacker_client.disconnect()

        # Give some time for the message to be received
        time.sleep(2)

        # Verify if the unauthorized message was detected as such
        self.assertEqual(self.legitimate_messages_received, 0, "No legitimate messages should have been received.")
        self.assertEqual(
            self.unauthorized_messages_received, 1,
            "One unauthorized message should have been received, indicating a potential integrity violation.")


if __name__ == "__main__":
    unittest.main()
