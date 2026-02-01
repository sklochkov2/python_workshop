def cpu_work_pure_python(text: str, rounds: int = 40) -> int:
    """
    Intentionally CPU-heavy Python bytecode work (GIL-bound).
    A silly rolling hash repeated many times.
    """
    acc = 0
    for _ in range(rounds):
        for ch in text:
            acc = (acc * 131 + ord(ch)) & 0xFFFFFFFF
    return acc
