import json
import random
import time
from pathlib import Path


WORDS = [
    "model", "inference", "latency", "vector", "embedding", "token", "cache", "queue",
    "request", "response", "timeout", "throughput", "python", "service", "feature",
    "ranking", "rerank", "classify", "error", "retry", "backoff", "schema", "index",
]

def make_text(rng: random.Random, min_words=20, max_words=120) -> str:
    n = rng.randint(min_words, max_words)
    return " ".join(rng.choice(WORDS) for _ in range(n))

def generate(out_path: Path, n: int = 20_000, seed: int = 42) -> None:
    rng = random.Random(seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    endpoints = ["/predict", "/embed", "/rerank", "/classify"]
    model_versions = ["v1", "v2", "v3"]
    user_count = 5_000
    now = int(time.time())

    with out_path.open("w", encoding="utf-8") as f:
        for i in range(n):
            user_id = f"user_{rng.randrange(user_count):05d}"
            latency_ms = int(30 + (rng.random() ** 6) * 2000)
            status = 200 if rng.random() > 0.01 else rng.choice([400, 401, 429, 500, 503])

            event = {
                "ts": now - rng.randint(0, 86400),
                "event_id": f"evt_{i:08d}",
                "user_id": user_id,
                "endpoint": rng.choice(endpoints),
                "model_version": rng.choice(model_versions),
                "status": status,
                "latency_ms": latency_ms,
                "prompt": make_text(rng),
            }
            f.write(json.dumps(event) + "\n")

if __name__ == "__main__":
    generate(Path("data/events.jsonl"), n=20_000, seed=42)
    print("Wrote data/events.jsonl")
