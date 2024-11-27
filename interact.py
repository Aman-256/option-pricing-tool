from web3 import Web3
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to the Ethereum Sepolia testnet
web3 = Web3(Web3.HTTPProvider(os.getenv("ALCHEMY_API_URL")))

if web3.is_connected():
    print("Connected to Ethereum network!")
else:
    print("Failed to connect.")



# Contract address 
contract_address = "0x84692A8c4cc52C78C4c2493a37c66428D1151345"  # Your deployed contract address

# Load the compiled contract ABI
with open("compiled_code.json", "r") as file:
    compiled_sol = json.load(file)

abi = compiled_sol['contracts']['OptionPricing.sol']['OptionPricing']['abi']

# Connect to the deployed contract
contract = web3.eth.contract(address=contract_address, abi=abi)

# Get the account details
private_key = os.getenv("PRIVATE_KEY")
account = web3.eth.account.from_key(private_key)
nonce = web3.eth.get_transaction_count(account.address)

# Check wallet balance in ETH
balance = web3.eth.get_balance(account.address)
print(f"Wallet Balance: {web3.from_wei(balance, 'ether')} ETH")



def create_option(strike_price, premium, expiration):
    premium_in_wei = web3.to_wei(premium, 'ether')
    
    # Set a manual gas limit
    gas_limit = 500000  # A reasonable upper bound for gas limit

    # Estimate gas cost
    gas_price = web3.eth.gas_price
    total_gas_cost = gas_limit * gas_price
    print(f"Estimated Gas Cost: {web3.from_wei(total_gas_cost, 'ether')} ETH")

    # Build the transaction
    transaction = contract.functions.createOption(strike_price, premium_in_wei, expiration).build_transaction({
        'chainId': 11155111,
        'from': account.address,
        'nonce': nonce,
        'value': premium_in_wei,
        'gasPrice': gas_price,
        'gas': gas_limit  # Manually set the gas limit
    })

    # Sign and send the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Option created in transaction: {tx_receipt.transactionHash.hex()}")




# Example: Get option details (Calling getOptionDetails function)
def get_option_details():
    option_details = contract.functions.getOptionDetails().call({'from': account.address})
    print(f"Option Details: Strike Price = {option_details[0]}, Premium = {option_details[1]}, Expiration = {option_details[2]}, Exercised = {option_details[3]}")

# Example usage: Creating an option with sample data
create_option(1000, web3.to_wei(0.0001, 'ether'), 86400)  # Example: Strike price = 1000, premium = 0.01 ETH, expiration = 2 days (in seconds)


#to check balance
balance = web3.eth.get_balance(account.address)
print(f"Wallet Balance: {web3.from_wei(balance, 'ether')} ETH")

gas_price = web3.eth.gas_price  # Get the current gas price
estimated_gas = contract.functions.createOption(1000, web3.to_wei(0.01, 'ether'), 172800).estimate_gas({
    'from': account.address,
    'value': web3.to_wei(0.01, 'ether')  # Value is equal to the premium
})

total_gas_cost = gas_price * estimated_gas
print(f"Estimated gas cost: {web3.from_wei(total_gas_cost, 'ether')} ETH")

# Example usage: Fetching option details
get_option_details()
