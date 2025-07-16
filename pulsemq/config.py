class Config:
    def __init__(
        self,
        bind_ip: str = "0.0.0.0",
        bind_port: int = 7896,
        ack_timeout_seconds: int = 10,
        time_between_acks_seconds: int = 3,
        log_level: str = "INFO",
        consumer_error_threshold: int = 100,
        consumer_error_timeout_seconds: int = 30,
    ):
        """Create a config which is used to intialise the broker. The default config
        binds to all interfaces on port 7896, has an ACK timeout of 10 seconds,
        uses INFO log level, and has a consumer error threshold of 100 with a timeout of 30 seconds.

        Args:
            bind_ip (str): The IP address to bind the broker to. Defaults to 0.0.0.0
            bind_port (int): The port to bind the broker to. Defaults to 7896
            ack_timeout_seconds (int): The timeout for ACKs in seconds. Defaults to 10, has to be greater than 3 and less than 600
            time_between_acks_seconds (int): The time between ACKs in seconds. Defaults to 3. Has to be greater than 1 and less than 600
            log_level (str): The logging level. Defaults to INFO. Must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL
            consumer_error_threshold (int): The number of errors a consumer can have before being disconnected
            consumer_error_timeout_seconds (int): The timeout in seconds a consumer has to recover from errors before being allowed to reconnect
        """

        self.bind_ip: str = bind_ip
        self.bind_port: int = bind_port
        self.ack_timeout_seconds: int = ack_timeout_seconds
        self.time_between_acks_seconds: int = time_between_acks_seconds
        self.log_level: str = log_level.upper()
        self.consumer_error_threshold: int = consumer_error_threshold
        self.consumer_error_timeout_seconds: int = consumer_error_timeout_seconds

        # check valid ACK timeout
        if not (3 < self.ack_timeout_seconds < 600):
            raise ValueError(
                "ACK timeout must be greater than 3 and less than 600 seconds."
            )

        # check valid time between acks
        if self.time_between_acks_seconds <= 1 or self.time_between_acks_seconds >= 600:
            raise ValueError(
                "Time between ACKs must be greater than 1 and less than 600 seconds."
            )

        # check valid port range
        if self.bind_port < 1 or self.bind_port > 65535:
            raise ValueError("Bind port must be between 1 and 65535.")

        # check valid ipv4 address
        import ipaddress

        try:
            ipaddress.ip_address(self.bind_ip)
        except ValueError:
            raise ValueError(f"Invalid IP address: {self.bind_ip}")

        # check valid log level
        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(
                f"Invalid log level: {self.log_level}. Must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL."
            )
