import sys
import logging
import logging.handlers
import network_connector


TTN_APP_KEY = "ttn-account-v2.ouYTdtAdlloUvoTdslOK-nsMZCAwah69vYkbKj2bN4k"
TTN_APPLICATION_ID = "lora-fing"
TTN_HOST = "us-west.thethings.network"



loglevel ='DEBUG'
logfile = "connector_log.txt"
logger = logging.getLogger(__name__)

t_network_connector = network_connector.TTNConnector(t_network_access_key=TTN_APP_KEY,
                                                                            t_network_id=TTN_APPLICATION_ID,
                                                                            t_network_host=TTN_HOST)


def start_connector():
    """ Starts a network connector with the parameters provided in the environment variables."""

    _aux_configure_log()
    t_network_connector.start_connector()


def _aux_configure_log():
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logger.setLevel(numeric_level)
    log_handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024000, backupCount=10)
    log_formatter = logging.Formatter('%(asctime)s - %(module)s:%(levelname)s: %(message)s')
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)

    # Logging information output to stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(numeric_level)
    formatter = logging.Formatter('%(asctime)s - %(module)s:%(levelname)s: %(message)s')
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    logger.info('Starting service Network Connector %s', "0")


if __name__ == "__main__":
    start_connector()
