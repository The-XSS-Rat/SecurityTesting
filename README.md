MAX_PAYLOAD_SIZE = 2048

def scan_payload(payload):
    # Limit payload size to prevent excessive processing
    return payload[:MAX_PAYLOAD_SIZE]