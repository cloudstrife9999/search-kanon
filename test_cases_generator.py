#!/usr/bin/env python3


import random
from hashlib import sha256


with open("test.txt", "w") as f:
    for i in range(1000000):
        f.write(sha256(bytes(str(i), "utf-8")).hexdigest() + "\n")