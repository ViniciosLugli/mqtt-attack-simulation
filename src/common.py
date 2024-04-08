import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self, client_id, broker_address="localhost", port=1891, override_on_connect=None, override_on_message=None):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id, reconnect_on_failure=False)
        self.broker_address = broker_address
        self.port = port

        self.client.on_connect = override_on_connect or self.on_connect
        self.client.on_message = override_on_message or self.on_message

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print(f"Connected with result code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}' with QoS {msg.qos}")

    def connect(self):
        self.client.connect(self.broker_address, self.port, 60)
        self.client.loop_start()

    def publish(self, topic, payload, qos=0, retain=False):
        print(f"Publishing message '{payload}' on topic '{topic}' with QoS {qos}")
        self.client.publish(topic, payload, qos, retain)

    def subscribe(self, topic, qos=0):
        self.client.subscribe(topic, qos)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()


if __name__ == "__main__":
    client_id = "python_publisher"
    broker_address = "localhost"
    port = 1891

    mqtt_client = MQTTClient(client_id, broker_address, port)
    mqtt_client.connect()
    mqtt_client.subscribe("test/topic")
    mqtt_client.publish("test/topic", "Hello MQTT!")

    import time
    time.sleep(10)

    mqtt_client.disconnect()
