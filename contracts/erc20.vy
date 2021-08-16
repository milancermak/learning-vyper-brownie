# @version ^0.2.0

from ..interfaces import IERC20

implements: IERC20

event Transfer:
    _from: indexed(address)
    _to: indexed(address)
    _value: uint256

event Approval:
    _owner: indexed(address)
    _spender: indexed(address)
    _value: uint256

name: public(String[128])
symbol: public(String[128])
decimals: public(uint256)
totalSupply: public(uint256)
balances: HashMap[address, uint256]
allowances: HashMap[address, HashMap[address, uint256]]


@external
def __init__(_name: String[128],
             _symbol: String[128],
             _decimals: uint256,
             _totalSupply: uint256):
    self.name = _name
    self.symbol = _symbol
    self.decimals = _decimals
    self.totalSupply = _totalSupply
    self.balances[msg.sender] = _totalSupply

    log Transfer(ZERO_ADDRESS, msg.sender, _totalSupply)


@view
@external
def balanceOf(_owner: address) -> uint256:
    return self.balances[_owner]


@external
def transfer(_to: address,
             _value: uint256) -> bool:
    assert self.balances[msg.sender] >= _value # "Not enough dough"

    self.balances[msg.sender] -= _value
    self.balances[_to] += _value

    log Transfer(msg.sender, _to, _value)
    return True


@external
def transferFrom(_from: address,
                 _to: address,
                 _value: uint256) -> bool:
    assert self.allowances[_from][msg.sender] >= _value # "No way"
    assert self.balances[_from] >= _value # "Not enough dough"

    self.allowances[_from][msg.sender] -= _value
    self.balances[_from] -= _value
    self.balances[_to] += _value

    log Transfer(_from, _to, _value)
    return True


@external
def approve(_spender: address,
            _value: uint256) -> bool:
    self.allowances[msg.sender][_spender] = _value

    log Approval(msg.sender, _spender, _value)
    return True


@view
@external
def allowance(_owner: address,
              _spender: address) -> uint256:
    return self.allowances[_owner][_spender]
