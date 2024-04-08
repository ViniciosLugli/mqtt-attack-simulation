# MQTT Attack Simulation

This project explores various attack scenarios on MQTT services, focusing on potential violations of the CIA Triad: Confidentiality, Integrity, and Availability. Each scenario is demonstrated through a Python script that simulates the specific attack vector.

## Questions and Scenarios

### What happens if you use the same ClientID on another machine or browser session?

Using the same ClientID from another location disconnects the first client, affecting the availability of the service for the initially connected client.

-   **CIA Triad Violation**: Availability
-   **Demonstration Script**: [src/001.py](./src/001.py)

### Can any pillar of the CIA Triad be easily violated with the resource parameters?

Sending too many messages or overly large messages can overload the system, similar to a DDoS attack, affecting its availability.

-   **CIA Triad Violation**: Availability
-   **Demonstration Script**: [src/002.py](./src/002.py)

### Without authentication, how can the confidentiality aspect be violated?

Allowing anonymous access (`allow_anonymous = true`) lets anyone join and listen to messages, violating confidentiality.

-   **CIA Triad Violation**: Confidentiality
-   **Demonstration Script**: [src/003and004.py](./src/003and004.py)

### Violation of the Confidentiality pillar

Joining an MQTT channel without authentication allows unauthorized access to messages, violating confidentiality.

-   **CIA Triad Violation**: Confidentiality
-   **Demonstration Script**: [src/003and004.py](./src/003and004.py)

### Violation of the Integrity pillar

Sending unauthorized or fake messages can deceive the system and its users, highlighting the need for message verification.

-   **CIA Triad Violation**: Integrity
-   **Demonstration Script**: [src/005.py](./src/005.py)

### Violation of the Availability pillar

Disrupting the service for others, either by connecting multiple times or flooding with messages, affects service availability.

-   **CIA Triad Violation**: Availability
-   **Demonstration Script**: [src/006.py](./src/006.py)

## Setup

To run the simulation scripts, you need:

-   Python 3.6 or later.
-   An MQTT broker running locally or accessible remotely( you can use the [docker-compose.yml](./docker-compose.yml) file to run a local Mosquitto broker).
-   The `paho-mqtt` Python package. Install it using `pip install paho-mqtt`.

## Running the Simulations

1. Clone the repository or download the scripts.
2. Ensure you have an MQTT broker running. For local testing, you can use Mosquitto, HiveMQ, or any other MQTT broker.
3. Adjust the broker address and port in the scripts if necessary. By default, they are set to `localhost` and `1883` (or `1891` as in the examples).
4. Run each script with Python to see the demonstrated attack scenario. For example:

```bash
python src/001.py
```

## Tests

Each script includes a simulation of an attack or a condition that might violate one of the CIA Triad's pillars. The code comments and print statements in each script provide insights into what each part of the script does and how it relates to the potential security violation.
