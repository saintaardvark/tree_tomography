#!/usr/bin/env python3

from time import sleep

import numpy as np


def main():
    """
    Main entry point
    """
    mu, sigma = 5, 1  # mean and standard deviation
    s = np.random.normal(mu, sigma, 1000)
    for num in s:
        print(f"{num:.02f}")

if __name__ == "__main__":
    main()
