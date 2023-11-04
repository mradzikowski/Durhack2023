from paho.mqtt import client as mqtt_client


def connect_mqtt() -> mqtt_client:
    logger.info("Connecting to MQTT Broker...")

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
        else:
            logger.info("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(env_variables.client_id, transport="tcp")
    client.on_connect = on_connect
    while True:
        try:
            client.connect(host=env_variables.emqx_ip, port=env_variables.emqx_port)
            logger.info("Connected to MQTT Broker as Subscriber!")
            break
        except Exception:
            logger.info("Cannot connect to MQTT Broker as Subscriber!")
            continue

    return client