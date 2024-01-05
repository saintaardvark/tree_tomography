#!/usr/bin/env python3

from time import sleep

import numpy as np


def main():
    """
    Main entry point
    """
    mu, sigma = 5, 1  # mean and standard deviation
    s = np.random.normal(mu, sigma, 1000)
    t = np.random.normal(mu, sigma, 1000)

    print(f"1->2,1->3")

    for num, othernum in zip(s, t):
        print(f"{num:.02f},{othernum:.02f}")


if __name__ == "__main__":
    main()
