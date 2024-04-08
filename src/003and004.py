import unittest
from common import MQTTClient
import threading
import time


class MQTTNoAuthConfidentialityTest(unittest.TestCase):
    broker_address = "localhost"
    port = 1891
    topic = "confidential/topic"

    def on_message(self, client, userdata, msg):
        self.received_messages.append(msg.payload.decode())

    def setUp(self):
        self.received_messages = []
        # Setup an unauthorized client that will try to listen on the confidential topic
        self.unauthorized_client = MQTTClient("unauthorized_client", self.broker_address, self.port, override_on_message=self.on_message)
        self.unauthorized_client.connect()
        self.unauthorized_client.subscribe(self.topic, qos=0)
        time.sleep(1)  # Wait for subscription to complete

    def tearDown(self):
        self.unauthorized_client.disconnect()

    def test_unauthorized_access_to_confidential_messages(self):
        # Simulate a legitimate client publishing a message to the confidential topic
        legit_client = MQTTClient("legitimate_client", self.broker_address, self.port)
        legit_client.connect()
        legit_client.publish(self.topic, "This is a confidential message", qos=0)
        legit_client.disconnect()

        # Give some time for the message to be received
        time.sleep(2)

        # Check if the unauthorized client received the message
        self.assertIn("This is a confidential message", self.received_messages,
                      "Unauthorized client should not have received confidential messages.")


if __name__ == "__main__":
    unittest.main()
