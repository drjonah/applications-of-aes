# Advanced Encryption Standard & Applications

Hello Everyone! When brainstorming potential projects, I stumbled upon cryptography and equivalent algorithms. I chose to study the Advanced Encryption Standard (or AES) because of its popularity. Another aspect is that it is virtually impossible to break when AES is pushed to its max. I was able to design an AES algorithm and apps that put it to "day-to-day" use. This helped me visualize and understand how this algorithm and other algorithms are vital in our world today.  


## Table of contents

- AES Versions
- Requirements
- Installation
- Configuration
- FAQ
- Credits


## AES Version
### ECB (Electronic Code Block) [Default]
This is the simplest form of AES encryption. This is the method where text is split into 16 byte code blocks and are encrypted separately. The downside of this method is it is the easiest method to reverse. Because every input has an identical outputs, patterns can be easily identified to those who know what to look for. This is known as having a lack of diffusion.
### CBC (Chipher Block Chaining) [Secure]
This is not the most advanced version of AES but it is way more secure than ECB because of one reason - initialization vectors. These vectors are encrypted into each code block. When the encryption begins, the plaintext is XORed this vector. The vector allows for more variation within each encryption. The vector must be the same for encrypting and decrypting.

## Requirements

AES requires no modules outside the python library.


## Installation 

1. Clone Repository: <br> `git clone https://github.com/drjonah/applications-of-aes.git`


## Configuration (required)

To costumize the key used in the encrypting and decrypting process, you add it in `config.json`. There is also an option to costumize an initialization vector (IV). This is used when `cbc` is marked `true`. More information is found under `"AES Versions"`.


## FAQ

**Q: How do I costumize the strength of the algorithm?**

**A:** The strength of aes algorithm depends on the length of the key.
<br>      Key Length 16: 128 bts, 2^128 combinations
<br>      Key Length 24: 192 bts, 2^192 combinations
<br>      Key Length 32: 256 bts, 2^256 combinations
<br>      Another way is a difference aes encryption version. This algorithm allows for CBC to be used. This can be changed in the same place as the key in `config.json`. Set `"CBC"` to `true` and make sure you have text in `IV`.

**Q: How do I generate a random key?**

**A:** Inside of `scripts/` there is a file titled "random_key.py".

**Q: How do I generate a random initialization vector (IV)?**

**A:** Inside of `scripts/` there is a file titled "random_iv.py".

**Q: How do I run test cases with the AES algorithm?**

**A:** Inside of `tests/` there are test files to utilize the AES algorithm.

**Q: How do I execute the application files?**

**A:** Each application has its own README.md with instructions.

## Credits

- [Government document](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf)
- [Galois implementation](http://blog.simulacrum.me/2019/01/aes-galois/)
- [Offical test vectors](https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Algorithm-Validation-Program/documents/aes/AESAVS.pdf )
- [My Stackoverflow question](https://stackoverflow.com/questions/76862154/why-is-my-aes-algorithm-not-producing-correct-output)
- JUSTYN!!!