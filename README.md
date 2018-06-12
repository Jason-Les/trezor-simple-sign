# trezor-simple-sign

## About
Very simple tool for signing messages and transactions with trezor. 
This was written using the SatoshiLab's python-trezor API available here: https://github.com/trezor/python-trezor

Please do not use for mainnet transactions without first reviewing and testing code yourself. Tool's intention is to be
a proof of concept, **NOT for regular use**. I have not added sufficient error-checking on input. I have done minimal testing.

Currently only supporting:

- P2PKH testnet addresses
- Single input (Single prev hash and index)
- Single output (with a single change address)

## Support
I have only tested this using python 3.6 on Ubuntu with Trezor One. I cannot yet vouch for reliability on other setups.

## Install
The python-trezor package is required to run this. Please follow install instructions for python-trezor here: https://github.com/trezor/python-trezor

## Future work
I wanted to get a very basic version up ASAP, so there is still additional work to be done. I intend to do the following:

- Add support for p2sh and wrapped segwit addresses
- Accept multiple inputs and allow multiple outputs
- Automatcially pull UTXOs from specified signing address
- Enable mainnet support
