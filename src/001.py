import unittest
from common import MQTTClient
import threading
import time


class MQTTAttackSimulationTest(unittest.TestCase):
    broker_address = "localhost"
    port = 1891
    topic = "test/topic"

    # Handler for the first client's connection callback
    def first_client_on_connect(self, client, userdata, flags, rc, properties=None):
        print("First client connected with result code", rc)
        self.first_client_connected = True

    # Handler for the second client's connection callback
    def second_client_on_connect(self, client, userdata, flags, rc, properties=None):
        print("Second client connected with result code", rc)
        self.second_client_connected = True

    # Test to simulate two clients connecting with the same ClientID
    def test_client_id_conflict(self):
        self.first_client_connected = False
        self.second_client_connected = False

        # Initialize the first client and override its on_connect method
        first_client = MQTTClient("conflict_client", self.broker_address, self.port, self.first_client_on_connect)
        first_thread = threading.Thread(target=first_client.connect)
        first_thread.start()

        # Wait a bit to ensure the first client has time to connect
        time.sleep(2)

        # Initialize the second client with the same ClientID and override its on_connect method
        second_client = MQTTClient("conflict_client", self.broker_address, self.port, self.second_client_on_connect)
        second_thread = threading.Thread(target=second_client.connect)
        second_thread.start()

        # Wait a bit to ensure the second client attempts to connect
        time.sleep(2)

        # Ensure the second client connected
        self.assertTrue(self.second_client_connected, "Second client should have connected successfully.")

        # Check if the first client got disconnected (indirectly, as we don't have a direct flag for disconnection)
        self.assertTrue(self.first_client_connected and not first_client.client.is_connected(),
                        "First client should have been disconnected.")

        # Clean up
        second_client.disconnect()
        first_client.disconnect()


if __name__ == "__main__":
    unittest.main()
