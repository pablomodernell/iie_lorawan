"""
Connector between the TTN transport network and the WS processing services (Message Subscriptor, dataserver, etc.).
"""
import logging

import paho.mqtt.client


DEFAULT_MQTT_KEEPALIVE = 60  # seconds
DEFAULT_MQTT_PORT = 1883


logger = logging.getLogger("connector_logger")


class TTNConnector(object):
    """
    Network connector that handles the connection between the WS data visualization
    and processing platform (e.g. Message Subscriptor + DataServer) and the The Things Network (TTN)
    network.
    """

    def __init__(self, t_network_id, t_network_access_key, t_network_host, from_device_id="+"):
        """
        Creates a connector that listen to the messages comming from a particular node (by default: "+", all nodes).
        All the connection parametes are obtained from environment variables.

        It sets a default keepalive of 60 seconds (maximum period in seconds between communications with the broker.
        If no other messages are being exchanged, this controls the rate at which the client will send ping messages
        to the broker.)

        It uses 1883 as a default mqtt server port (the network port of the server host to connect to).

        :param from_device_id: string ID of the node to receive its messages (by default "+" means all nodes).
        """
        self.mq_client = paho.mqtt.client.Client()
        self._mqtt_client_keepalive = DEFAULT_MQTT_KEEPALIVE
        self._mqtt_client_port = DEFAULT_MQTT_PORT
        self.mq_client.on_connect = self._on_connect
        self.mq_client.on_message = self._on_message
        self.t_network_id = t_network_id
        self.t_network_access_key = t_network_access_key
        self.t_network_host = t_network_host
        self.from_device_id = from_device_id

        self.mq_client.username_pw_set(self.t_network_id, self.t_network_access_key)

    def start_connector(self):
        """
        Registers the connector to the transport network and starts a loop waiting for messages from it.
        It also starts the downlink listener to receive downlink messages comming from the processing services to
        the network.
        """
        self.mq_client.connect(self.t_network_host, port=self._mqtt_client_port, keepalive=self._mqtt_client_keepalive)
        self.mq_client.loop_forever()

    def publish_to_network(self, to_device_id, downlink_message):
        """
        Send messages to a device in the network.
        :param to_device_id: string device identification.
        :param downlink_message: message to be sent.
        :return:
        """
        self.mq_client.publish(topic=self.t_network_id + "/devices/" + to_device_id + "/down",
                               payload=downlink_message)

    def _on_connect(self, client, userdata, flags, rc):
        """ Connection callback function executed when the client connects."""
        logger.info("Connected with result code " + str(rc))
        client.subscribe(self.t_network_id + "/devices/" + self.from_device_id + "/up")

    def _on_message(self, client, userdata, msg):
        """ Callback excecuted every time that a message is received."""
        logger.info("On message, >>>>>>>>\n")
        self.up_message_callback(msg=msg)

    def up_message_callback(self, msg):
        """
        Handles the uplink messages from TTN and convert them to the format used
        by WS platform.
        """
        logger.debug("Processing message from TTNConnector.")
        logger.info("Topic: " + msg.topic + "\n")
        logger.info("Received str from TTN: {}".format(str(msg.payload)))
        logger.info("->>>>>>>>\n\n")


