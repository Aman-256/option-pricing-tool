from web3 import Web3
from solcx import compile_standard
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to the Sepolia network via Alchemy
web3 = Web3(Web3.HTTPProvider(os.getenv("ALCHEMY_API_URL")))

# Check if connected
if web3.is_connected():
    print("Connected to Ethereum network!")
else:
    print("Failed to connect.")

# Solidity contract code (SimpleStorage.sol)
simple_storage_code = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 private storedNumber;

    function setNumber(uint256 _number) public {
        storedNumber = _number;
    }

    function getNumber() public view returns (uint256) {
        return storedNumber;
    }
}
'''

# Compile the Solidity contract
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"SimpleStorage.sol": {"content": simple_storage_code}},
    "settings": {"outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}}},
})

# Get bytecode and ABI
bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']
abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']

# Get the private key and the account
private_key = os.getenv("PRIVATE_KEY")
print(f"Private Key: {private_key}")

account = web3.eth.account.from_key(private_key)

# Get the latest nonce
nonce = web3.eth.get_transaction_count(account.address)

# Build contract deployment transaction
contract = web3.eth.contract(abi=abi, bytecode=bytecode)
transaction = contract.constructor().build_transaction({
    "chainId": 11155111,  # Sepolia testnet chain ID
    "from": account.address,
    "nonce": nonce,
    "gasPrice": web3.eth.gas_price
})

# Sign the transaction
signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

# Send the transaction
tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

# Wait for the transaction receipt
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Contract deployed to: {tx_receipt.contractAddress}")
