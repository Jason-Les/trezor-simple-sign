'''
Very simple commandline tool for signing messages and Bitcoin transactions with Trezor

Please do not use for mainnet transactions without first reviewing and testing code yourself. Tool's intention is to be
a proof of concept, not for regular use. I have not added sufficient error-checking on input.

Currently only supporting:

-P2PKH addresses
-Single input (Single prev hash and index)
-Single output (with a single change address)

By: Jason Les
JasonLes@gmail.com
@heyitscheet
'''

import binascii
from trezorlib.client import TrezorClient
from trezorlib.tx_api import TxApiBlockCypher
from trezorlib.transport_hid import HidTransport
import trezorlib.messages as proto_types
import itertools
import argparse
import base64


# Take a target address as input and search the client until a matching bip32 path is found, then return it
def find_path(target_address, client, coin='Testnet'):

    if coin == 'Testnet':
        base_path = "44'/1'"
    if coin == 'Bitcoin':
        base_path = "44'/0'"
    # Searches up to 5 accounts and 100 addresses for each (including change addresses)
    for acct, addr, chng in itertools.product(range(5), range(100), range(2)):
        curr_path = base_path + "/{}'/{}/{}".format(acct, chng, addr)
        # print(curr_path)
        bip32_path = client.expand_path(curr_path)
        curr_addr = client.get_address(coin, bip32_path)
        if curr_addr == target_address:
            return bip32_path

    # Return None if search exhausts with no match
    return None

def sign(addr, msg, tx):
    # List all connected Trezors on USB
    devices = HidTransport.enumerate()

    # Check whether we found any trezor devices
    if len(devices) == 0:
        print
        'No TREZOR found'
        return

    # Use first connected device
    transport = devices[0]

    # Determine coin/address type corresponding to signing addresses
    # TODO: Enable mainnet addresses. Currently temporarily disabled for safety.
    prefix = addr[0]
    if prefix == '1' or prefix == '3':
        # coin = 'Bitcoin'
        raise ValueError('Mainnet temporarily disabled until more testing and work is done')
    if prefix == 'm' or prefix == 'n':
        coin = 'Testnet'

    # Creates object for manipulating trezor
    client = TrezorClient(transport)
    if coin == 'Testnet':
        TxApi= TxApiBlockCypher(coin, 'https://api.blockcypher.com/v1/btc/test3/')
        print('Making testnet api')
    # if coin == 'Bitcoin':
        # TxApi = TxApiBlockCypher(coin, 'https://api.blockcypher.com/v1/btc/main/')
        # print("Making bitcoin api")

    # Set the api for trezor client
    client.set_tx_api(TxApi)

    # Find the bip32 path of the address we are signing a message or tx from
    found_path = find_path(target_address=addr, client=client, coin=coin)
    if found_path is None:
        raise ValueError('The address {} was not found on the connected trezor {} in search for its bip32 path'.format(addr,transport))
    else:
        print('Found bip32 path for: {} - signing from this address'.format(client.get_address(coin, found_path)))

    # Sign the specified message from the specified source address. Signature is in base64
    # TODO: In both message and transaction sign, add support for script types besides just P2PKH
    if msg is not None:
        res = client.sign_message(coin_name=coin, n=found_path, message=msg)
        print('Signing message: "{}"\nFrom address: {}'.format(msg, addr))
        print('Signature:', str(base64.b64encode(res.signature), 'ascii'))

    if tx is not None :
        # In this basic implementation, remember that tx data comes in the format:
        # <PREV HASH> <PREV INDEX> <DESTINATION ADDRESS> <AMOUNT>
        prev_hash = tx[0]
        prev_index = int(tx[1])
        dest_address = tx[2]
        send_amount = int(tx[3])

        # TODO: Remove fee constant of 650 satoshi and accept custom input
        fee = 650
        # Uses blockcypher API to get the amount (satoshi) of the UTXO
        utxo_amount = TxApi.get_tx(prev_hash).bin_outputs[0].amount

        if send_amount + fee > utxo_amount:
            raise ValueError('UTXO amount of {} is too small for sending {} satoshi with {} satoshi fee'.format(utxo_amount, send_amount, fee))

        # Determine amount to send to change address
        change = utxo_amount - send_amount - fee

        print('Using UTXO: {} and index {} to send {} {} coins to: {}'.format(prev_hash, prev_index, send_amount / 100000000, coin, dest_address))

        # The inputs of the transaction.
        inputs = [
            proto_types.TxInputType(
                address_n=found_path,
                prev_hash=binascii.unhexlify(prev_hash),
                prev_index=prev_index,
            ),
        ]
        # The outputs of the transaction
        # TODO: Handle alternative (segwit) output types
        output_type = proto_types.OutputScriptType.PAYTOADDRESS

        outputs = [
            proto_types.TxOutputType(
                amount=send_amount,  # Amount is in satoshis
                script_type=output_type,
                address=dest_address
            ),
        ]
        # Add change output
        # Sends change to change address on the bip32 path of the sending address
        if change > 0:
            change_path = found_path[:]
            change_path[3] = 1
            change_address = client.get_address(coin, change_path)

            outputs.append(proto_types.TxOutputType(
                amount=change,
                script_type=output_type,
                address=change_address
            ))
            print('Sending change amount of {} {} coins to change address: {}'.format(change / 100000000, coin, change_address))

        # All information is ready, sign transaction and print it
        print('Verify transaction on your trezor')
        (signatures, serialized_tx) = client.sign_tx(coin, inputs, outputs)
        # print('Signatures:', signatures)
        print('Signed transaction:', serialized_tx.hex())

    client.close()


def main():
    # Arguments for command-line use
    # TODO: Add handling for multiple inputs, outputs, and custom fees
    parser = argparse.ArgumentParser(description='Sign a message or simple transaction with trezor')
    parser.add_argument("--addr", "-a", action='store', dest='addr',
                        help="Address to sign from", required=True)
    parser.add_argument("--msg", "-m", action='store', dest='msg',
                        help='Sign the following message (in quotes): "Message"')
    parser.add_argument("--tx", "-t", dest='tx', nargs=4,
                        help='Sign the following transaction in the format: <PREV HASH> <PREV INDEX> <DESTINATION ADDRESS> <AMOUNT>')

    # Parse passed arguments
    args = parser.parse_args()
    signing_addr = args.addr
    msg = args.msg
    tx = args.tx

    if msg is None and tx is None:
        raise RuntimeError('No signing operation inputted, nothing to do')

    # Perform signing of message and/or transaction
    sign(signing_addr, msg, tx)


if __name__ == '__main__':
    main()
