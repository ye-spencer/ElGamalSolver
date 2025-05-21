# ElGamalSolver

A lightweight Python tool to solve the discrete logarithm problem in small finite fields and recover private keys in ElGamal encryption.

## Overview

Given the public parameters of an ElGamal key `(p, g, h)` such that h ≡ g^x mod p this script finds the secret exponent `x` using the Pohlig-Hellman attack, utilizing the Chinese Remainder Theorem and the Baby-Step-Giant-Step algorithm. It demonstrates how weak or small key parameters can compromise cryptographic security.



