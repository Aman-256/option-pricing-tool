// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract OptionPricing {
    struct Option {
        address buyer;
        uint256 strikePrice;
        uint256 premium;
        uint256 expiration;
        bool exercised;
    }

    mapping(address => Option) public options;

    function createOption(uint256 _strikePrice, uint256 _premium, uint256 _expiration) public payable {
        require(msg.value == _premium, "Send exact premium");
        options[msg.sender] = Option(msg.sender, _strikePrice, _premium, _expiration, false);
    }

    function exerciseOption() public {
        Option storage option = options[msg.sender];
        require(block.timestamp <= option.expiration, "Option expired");
        require(!option.exercised, "Option already exercised");
        option.exercised = true;
    }

    function getOptionDetails() public view returns (uint256, uint256, uint256, bool) {
        Option storage option = options[msg.sender];
        return (option.strikePrice, option.premium, option.expiration, option.exercised);
    }
}
