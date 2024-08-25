from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[2] / "docker" / "bet_maker" / ".env"

MQ_ROUTING_KEY = "mq_events_queue"

EVENTS = {}
