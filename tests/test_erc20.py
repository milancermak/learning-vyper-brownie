import brownie
from brownie import accounts, erc20
import pytest

TOKEN_NAME = "TeeTee"
TOKEN_SYMBOL = "TT"
TOKEN_DECIMALS = 1
TOKEN_SUPPLY = int(1e18)


@pytest.fixture
def owner():
    return accounts[0]


@pytest.fixture
def token(owner):
    contract = owner.deploy(
        erc20, TOKEN_NAME, TOKEN_SYMBOL, TOKEN_DECIMALS, TOKEN_SUPPLY
    )
    return contract


def assert_transfer_event(tx, from_addr, to_addr, value):
    assert "Transfer" in tx.events
    event = tx.events["Transfer"]
    assert event["_from"] == from_addr
    assert event["_to"] == to_addr
    assert event["_value"] == value


def assert_approval_event(tx, owner_addr, spender_addr, value):
    assert "Approval" in tx.events
    event = tx.events["Approval"]
    assert event["_owner"] == owner_addr
    assert event["_spender"] == spender_addr
    assert event["_value"] == value


def test_init(token):
    assert token.name() == TOKEN_NAME
    assert token.symbol() == TOKEN_SYMBOL
    assert token.decimals() == TOKEN_DECIMALS
    assert token.totalSupply() == TOKEN_SUPPLY
    assert token.balanceOf(accounts[0]) == TOKEN_SUPPLY


def test_transfer(token, owner):
    to = accounts[1]
    value = 1e10

    assert token.balanceOf(to, {"from": to}) == 0
    tx = token.transfer(to, value, {"from": owner})

    assert tx.return_value is True
    assert token.balanceOf(to, {"from": owner}) == value
    assert token.balanceOf(owner, {"from": owner}) == TOKEN_SUPPLY - value
    assert_transfer_event(tx, owner.address, to.address, value)


def test_transfer_not_enough(token, owner):
    to = accounts[1]
    value = TOKEN_SUPPLY + 1

    assert token.balanceOf(owner, {"from": owner}) == TOKEN_SUPPLY
    with brownie.reverts():
        token.transfer(to, value, {"from": owner})


def test_approve(token, owner):
    spender = accounts[1]
    value = 1_000_000

    assert token.allowance(owner, spender, {"from": owner}) == 0
    tx = token.approve(spender, value, {"from": owner})

    assert tx.return_value is True
    assert token.allowance(owner, spender, {"from": owner}) == value
    assert_approval_event(tx, owner.address, spender.address, value)


def test_transferFrom(token, owner):
    recipient = accounts[1]
    delegate = accounts[2]
    value = 1_000_000
    initial_balance = token.balanceOf(owner, {"from": owner})
    token.approve(delegate, value, {"from": owner})

    tx = token.transferFrom(owner, recipient, value, {"from": delegate})

    assert tx.return_value is True
    assert token.allowance(owner, delegate, {"from": owner}) == 0
    assert token.balanceOf(owner, {"from": owner}) == initial_balance - value
    assert token.balanceOf(recipient, {"from": recipient}) == value
    assert_transfer_event(tx, owner.address, recipient.address, value)


def test_transferFrom_not_enough_balance(token):
    recipient = accounts[1]
    delegate = accounts[2]
    source = accounts[3]
    value = 1_000_000

    token.approve(delegate, value, {"from": source})

    with brownie.reverts():
        token.transferFrom(source, recipient, value, {"from": delegate})


def test_transferFrom_no_approval(token, owner):
    recipient = accounts[1]
    delegate = accounts[2]
    value = 1_000_000

    with brownie.reverts():
        token.transferFrom(owner, recipient, value, {"from": delegate})
