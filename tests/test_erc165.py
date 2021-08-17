from brownie import accounts, erc165test
import web3
import pytest


@pytest.fixture
def contract165():
    return accounts[0].deploy(erc165test)


def calculate_selector(s):
    return web3.Web3.keccak(text=s)[:4]


def xor_selectors(selectors):
    r = 0
    for s in selectors:
        r ^= int.from_bytes(calculate_selector(s), "big")
    return r


def test_supportsInterface(contract165):
    erc165_interface = "0x01ffc9a7"
    return_value = contract165.supportsInterface(
        erc165_interface, {"from": accounts[0]}
    )
    assert return_value is True


def test_custom_selectors(contract165):
    interface = hex(xor_selectors(["name", "storage", "addTwo(uint256)"]))
    return_value = contract165.supportsInterface(interface, {"from": accounts[0]})
    assert return_value is True


def test_not_supporting(contract165):
    interface = hex(xor_selectors(["addMore(uint256)"]))
    return_value = contract165.supportsInterface(interface, {"from": accounts[0]})
    assert return_value is False
