from os import getenv

# Rabbit Specific Values
rabbit_host = getenv("MQ_HOST", "localhost")
rabbit_port = getenv("MQ_PORT", 5672)
rabbit_queue = getenv("MQ_QUEUE", "XXX")

rabbit_queue_definitions = {
    m6_enriched_queue = getenv("MQ_QUEUE1", "M6_Enriched"),
    m6_raw_events_queue = getenv("MQ_QUEUE2", "M6_Raw_Events"),
    m6_dead_letter_queue = getenv("MQ_QUEUE3", "M6_Dead_Letter")
}

rabbit_username = getenv("MQ_USERNAME", "XXX")
rabbit_password = getenv("MQ_PASSWORD", "XXX")
rabbit_exchange = getenv("MQ_EXCHANGE", "XXX")
rabbit_routing_key = getenv("MQ_ROUTING_KEY", "XXX")
rabbit_vhost = getenv("MQ_VHOST", "XXX")

# Application Specific Values
last_tweet_id_filename = getenv("FILENAME", "XXX")
log_file = getenv("LOG_FILE", "mtw.log")
