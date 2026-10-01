from collections.abc import Iterator


def naive(p: str, t: str) -> Iterator[int]:
    for i in range(len(t) - len(p) + 1):
        for j in range(len(p)):
            if p[j] != t[i + j]:
                break
        else:
            yield i
