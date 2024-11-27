from solcx import compile_standard, install_solc
import json

# Install Solidity compiler version 0.8.0
# install_solc('0.8.0')  # No need to install if using Homebrew-installed solc

# Load the Solidity code
with open('./contracts/OptionPricing.sol', 'r') as file:
    option_pricing_code = file.read()

# Compile the contract
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"OptionPricing.sol": {"content": option_pricing_code}},
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }
        }
    }
})

# Save the compiled code to a JSON file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

print("Contract compiled successfully!")
