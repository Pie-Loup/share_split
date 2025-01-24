Secret sharing library for seed phrases
======

A Python3 project for sharing seed phrases. This project uses [Shamir's secret sharing scheme](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing).
It is a fork of the [following repository](https://github.com/jqueiroz/python-sslib)

## How to use
### Overview
For the mathematical details, check the source repo. This repo focuses on a practical implementation for spliting seed to shares in order to securely store seeds.

Run `main.py` and follow the instructions!

You can:
- Build shares from a seed or rebuild the seed from shares.
- Encrypt the shares so that you can safely communicate the shares online. Make sure to use a long enough passphrase to encrypt the shares if you do so.
- Decrypt a share if you receive an encrypted share. Storing a decrypted share is perfectly safe. Displaying a decrypted share online is fine but that exposes part of the puzzle needed to rebuild the seed.
- A QR code generation option is included to safely pass information from a disconnected computer to a phone.

### Usage

Let's take a main use case: split a seed into 3 of 5, this means the seed is split into 5 parts, of which 3 are needed to build back the seed.

#### Splitting seed into shares
The main parameters are the **required** shares and the **total** shares:
- The required number of shares is the number of shares you need to be able to build back your seed. Be careful when chosing this number. If you give enough shares to people so that they can rebuild the seed without you, you have to trust those people!
- The total number of shares is the number of puzzle pieces that are going to be generated. You should choose as many as you want distribute to places / people.

You can choose to encrypt the shares so that you can safely communicate those to a recipient without risk of being compromised. Make sure to note the passphrase somewhere or to ask the recipient to decrypt the share with the passphrase. Find another canal to communicate the passphrase.

#### Recovering secret from shares

You can easily recover the seed from the shares by inputing the shares one by one. You can also decrypt directly the shares while building the seed. This assumes all shares have the same passphrase

#### Decrypt a share
You can receive an encrypted share. Use this option to decrypt the share and store it decrypted. This ensure you don't need to remember yet another passphrase.

#### Prime modulus
To simplify secret sharing, the prime mod is fixed to the Mersen number 2203 so that you don't have to store yet another number. If your seed phrase is too large, you can increase or remove the prime mod input, but be sure to remember it when decrypting!

### Limitations
- No way to know if the seed entered it the correct one. Need to implement a public key/address generation to double check
- Only one passphrase for all shares
- No iteration on required shares that could simplify the rebuilding of the seed (no need to remember this)
- QR code generated may be too large for a small screen
- No "share rebuilding". If a share is lost, you have to rebuild the seed and then rebuild the shares.

### Warning
- Showing/storing enough shares on the same place not encrypted is akin to showing your seed! Just don't do it.
- **Set of shares generated are not necessarily compatible with one another! This means if you loose one share and want to redistribute it, you have to regenerate all the shares at once from the seed and distribute those. You can delete the previous ones. If you don't know the seed, then collect the shares, build the seed and rebuild the shares**
