# trezor-simple-sign

Very simple tool for signing messages and transactions with trezor 

Please do not use for mainnet transactions without first reviewing and testing code yourself. Tool's intention is to be
a proof of concept, not for regular use. I have not added sufficient error-checking on input.

Currently only supporting:

-P2PKH testnet addresses
-Single input (Single prev hash and index)
-Single output (with a single change address)

This was written using the SatoshiLab's python-trezor API available here: https://github.com/trezor/python-trezor

The python-trezor package is required to run this. Please follow install instructions on their page.