"""Random tests: the stack algorithm must match brute force at every range."""
import random
from break_even_envelope import minimal_envelope, brute_force_check, EXAMPLE


def test_example():
    lines, q = minimal_envelope(EXAMPLE)
    assert [a[0] for a in lines] == ["Boyne City", "Portland", "Lake Tahoe"]
    assert q == [25_000, 44_000]


def test_random():
    rng = random.Random(42)
    for _ in range(5000):
        n = rng.randint(1, 10)
        data = [(f"A{k}", rng.randint(0, 100), rng.randint(0, 100)) for k in range(n)]
        lines, q = minimal_envelope(data)
        brute_force_check(data, lines, q)


if __name__ == "__main__":
    test_example()
    test_random()
    print("All tests passed")
