import json
import random
import time
from pathlib import Path

def generate(out_path: Path, n: int = 300_000, seed: int = 42) -> None:
    random.seed(seed)
    model_versions = ["v1", "v2", "v3"]
    endpoints = ["/predict", "/embed", "/rerank", "/classify"]
    users = [f"user_{i:05d}" for i in range(20_000)]

    now = int(time.time())
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8") as f:
        for _ in range(n):
            user_id = random.choice(users)
            endpoint = random.choice(endpoints)
            model = random.choice(model_versions)

            # Latency: mostly fast, sometimes slow (long tail)
            base = random.random()
            latency_ms = int(30 + (base ** 6) * 2000)

            # Errors: some endpoints + high latency correlate with failures
            status = 200
            if random.random() < (0.005 + (latency_ms > 800) * 0.02):
                status = random.choice([400, 401, 429, 500, 503])

            # Payload-ish sizes: pretend it’s tokens/bytes
            input_tokens = int(20 + random.random() * 2000)
            output_tokens = int(5 + random.random() * 800)

            event = {
                "ts": now - random.randint(0, 86400),
                "request_id": f"req_{random.getrandbits(64):016x}",
                "user_id": user_id,
                "endpoint": endpoint,
                "model_version": model,
                "status": status,
                "latency_ms": latency_ms,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
            }
            f.write(json.dumps(event) + "\n")

if __name__ == "__main__":
    generate(Path("data/inference_logs.jsonl"), n=300_000)
