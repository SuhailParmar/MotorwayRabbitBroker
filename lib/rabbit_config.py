from os import getenv

# Rabbit Specific Values
rabbit_host = getenv("MQ_HOST", "localhost")
rabbit_port = getenv("MQ_PORT", 5672)
rabbit_mport = getenv("MQ_MPORT", 15672)

rabbit_queue_definitions = [
    getenv("MQ_QUEUE1", "M6_Enriched"),
    getenv("MQ_QUEUE2", "M6_Raw_Events"),
    getenv("MQ_QUEUE3", "M6_Dead_Letter")
]

# Routing key for each queue
rabbit_rk_definitions = [
    getenv("MQ_RK1", "M6_Enriched"),
    getenv("MQ_RK2", "M6_Raw"),
    getenv("MQ_RK3", "M6_DL")
]

rabbit_image = getenv("MQ_IMAGE", "rabbitmq:3.7-management")
rabbit_username = getenv("MQ_USERNAME", "guest")
rabbit_password = getenv("MQ_PASSWORD", "guest")
rabbit_exchange = getenv("MQ_EXCHANGE", "MotorwayExchange")
rabbit_vhost = getenv("MQ_VHOST", "motorway_vhost")

# Application Specific Values
log_file = getenv("LOG_FILE", "rabbit.log")
