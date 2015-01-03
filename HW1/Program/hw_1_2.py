#! /usr/bin/env python3
import hw_1_1 as dist

L = ("ACCGFDERAE", "ACDCGFERAE")
S = ("ECDACEGARF", "ECDACERGAF", "EECDACGARF", "EECDACRGAF")

if __name__ == "__main__":
    distance = [(l, s, dist.get_kendall_tau_dist(l,s)[0]) for l in L for s in S]
    print(distance)
