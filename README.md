# Advanced Encryption Standard & Applications

Hello Everyone! When brainstorming potential projects, I stumbled upon cryptography and equivalent algorithms. I chose to study the Advanced Encryption Standard (or AES) because of its popularity. Another aspect is that it is virtually impossible to break when AES is pushed to its max. I was able to design an AES algorithm and apps that put it to "day-to-day" use. This helped me visualize and understand how this algorithm and other algorithms are vital in our world today.  


## Table of contents

- Requirements
- Installation
- Configuration
- FAQ
- Credits


## Requirements

The applications of AES require the following modules:
- [TBD](https://www.google.com/)

AES requires no modules outside the python library.


## Installation 

1. Clone Repository: <br> `git clone https://github.com/drjonah/applications-of-aes.git`
2. Install Dependancies: <br> `pip install -r requirements.txt`


## Configuration (required)

To costumize the key used in the encrypting and decrypting process, you add it in `config.json`.


## FAQ

**Q: How do I costumize the strength of the algorithm?**

**A:** The strength of aes algorithm depends on the length of the key.
<br>      Key Length 16: 128 bts, 2^128 combinations
<br>      Key Length 24: 192 bts, 2^192 combinations
<br>      Key Length 32: 256 bts, 2^256 combinations

**Q: How do I generate a random key?**

**A:** Inside of `scripts/` there is a file titled "random_key.py".

## Credits

- [Government document](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf)
- [Galois implementation](http://blog.simulacrum.me/2019/01/aes-galois/)
- [Offical test vectors](https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Algorithm-Validation-Program/documents/aes/AESAVS.pdf )
- [My Stackoverflow question](https://stackoverflow.com/questions/76862154/why-is-my-aes-algorithm-not-producing-correct-output)