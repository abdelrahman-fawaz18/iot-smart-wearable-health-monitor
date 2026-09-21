# Node-RED integration

The Raspberry Pi deployment used Node-RED for sensor triggering, message formatting, CSV export, debug output, MQTT transport, and browser-based monitoring.

![Node-RED temperature flow](assets/node-red-temperature-flow.png)

The documented temperature path contains:

1. An inject node that supplies the sampling timestamp.
2. An MLX90614 input node that reads object and ambient temperature.
3. A function node that formats the payload.
4. Dashboard, debug, CSV, and file outputs.

The IMU flow follows the same acquisition pattern and adds an MQTT output node for downstream processing.
