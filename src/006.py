import unittest
from common import MQTTClient
import threading
import time


class MQTTPublisher:
    def __init__(self, client_id, broker_address, port, topic, message, count):
        self.client = MQTTClient(client_id, broker_address, port)
        self.topic = topic
        self.message = message
        self.count = count

    def run(self):
        self.client.connect()
        for _ in range(self.count):
            self.client.publish(self.topic, self.message)
            time.sleep(0.01)  # Avoid flooding too fast
        self.client.disconnect()


class MQTTAvailabilityTest(unittest.TestCase):
    broker_address = "localhost"
    port = 1891
    topic = "availability/test"

    def setUp(self):
        self.legitimate_client = MQTTClient("legitimate_client", self.broker_address, self.port)
        self.legitimate_client.connect()
        time.sleep(1)  # Ensure the client is connected

    def tearDown(self):
        self.legitimate_client.disconnect()

    def test_service_availability_under_attack(self):
        # Start multiple attackers in separate threads
        attackers = [MQTTPublisher(f"attacker_{i}", self.broker_address, self.port, self.topic, "Disrupt!", 100) for i in range(10)]
        for attacker in attackers:
            threading.Thread(target=attacker.run).start()

        # Try to use the service as a legitimate user during the attack
        start_time = time.time()
        self.legitimate_client.publish(self.topic, "Legitimate message")
        operation_time = time.time() - start_time

        # Allow some time for attackers to complete
        time.sleep(5)

        # Assert if the operation time is significantly higher, indicating service degradation
        self.assertLess(operation_time, 1, "Service operation time during attack is too high, indicating potential availability issue.")


if __name__ == "__main__":
    unittest.main()
