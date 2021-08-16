# @version ^0.2.0

# https://eips.ethereum.org/EIPS/eip-20
interface IERC20:
    def name() -> String[128]: view
    def symbol() -> String[128]: view
    def decimals() -> uint256: view
    def totalSupply() -> uint256: view
    def balanceOf(_owner: address) -> uint256: view
    def transfer(_to: address,
                 _value: uint256) -> bool: nonpayable
    def transferFrom(_from: address,
                     _to: address,
                     _value: uint256) -> bool: nonpayable
    def approve(_spender: address,
                _value: uint256) -> bool: nonpayable
    def allowance(_owner: address,
                  _spender: address) -> uint256: view
