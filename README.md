# trezor-simple-sign

## About
Very simple command-line tool for signing messages and transactions with trezor. 
This was written using the SatoshiLab's python-trezor (trezorlib) API available here: https://github.com/trezor/python-trezor

Please do not use for mainnet transactions without first reviewing and testing code yourself. Tool's intention is to be
a proof of concept, **NOT for regular use**. I have not added sufficient error-checking on input. I have done minimal testing.

Currently only supporting:

- Sending to P2PKH testnet addresses
- Single input (Single prev hash and index)
- Single output (with a single change address)

## Support
I have only tested this using python 3.6 on Ubuntu with Trezor One. I cannot yet vouch for reliability on other setups.

## Install
The python-trezor (trezorlib) package is required to run this. Please follow install instructions for python-trezor here: https://github.com/trezor/python-trezor

## Use
Use from command line as follows:
```
python3 trezor_sign.py -a <SOURCE ADDRESS> -m "Message to sign" -t <PREV HASH> <PREV INDEX> <DESTINATION ADDRESS> <AMOUNT IN SATOSHIS>
```
From command line, use `python3 trezor_sign.py -h` or `--help` for help as well

Example use:
```
python3 trezor_sign.py -a mwQRohxiG2NDJtEbaj3yUyPqyFN1xdtVq5 -t a9b488954842f73264023c5dbfeb319fae8a6cd0c2a80449e0691401c706fb5d 0 mtH9P9zeY4HdU4roE5BTYXfbDmfQZpZuEz 20000000
```

## Future work
I wanted to get a very basic version up ASAP, so there is still additional work to be done. I intend to do the following:

- Add full support for p2sh and wrapped segwit addresses
- Accept multiple inputs and allow multiple outputs
- Automatcially pull UTXOs from specified signing address
- Enable mainnet support

## Updates
#####June 13, 2018
You can now sign from p2sh-segwit addresses as well as take P2SH-segwit inputs however still can only have ouputs of P2PKH at this time