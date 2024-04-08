import unittest
from common import MQTTClient
import threading
import time


class MQTTResourceAttackTest(unittest.TestCase):
    broker_address = "localhost"
    port = 1891
    topic = "test/topic"

    def setUp(self):
        # Setup is called before each test method
        self.client = MQTTClient("test_client", self.broker_address, self.port)
        self.client.connect()
        time.sleep(1)  # Wait for connection to establish

    def tearDown(self):
        # Cleanup after each test method
        self.client.disconnect()

    def send_massive_messages(self, message_count, message_size):
        attacker_client = MQTTClient("attacker_client", self.broker_address, self.port)
        attacker_client.connect()
        message = "A" * message_size
        for _ in range(message_count):
            attacker_client.publish(self.topic, message, qos=0)
            time.sleep(0.01)  # Small delay
        attacker_client.disconnect()

    def test_legitimate_use_during_attack(self):
        # Start the attack in a background thread
        attack_thread = threading.Thread(target=self.send_massive_messages, args=(1000, 100))  # Simulated attack parameters
        attack_thread.start()

        # Measure time taken for legitimate operations
        start_time = time.time()
        self.client.publish(self.topic, "Test message from legitimate client", qos=1)
        self.client.subscribe(self.topic, qos=1)
        operation_time = time.time() - start_time

        # Wait for the attack to conclude before making assertions
        attack_thread.join()

        # Assert if the operation time is significantly higher, indicating service degradation
        # Note: This is a simple example, and in a real-world scenario, the threshold would be more carefully determined
        self.assertLess(operation_time, 5, "Operation time during attack is too high, indicating potential service degradation.")


if __name__ == "__main__":
    unittest.main()
