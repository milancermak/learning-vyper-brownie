# @version ^0.2.0

from ..interfaces import IERC165


implements: IERC165


storage: public(uint256)


@view
@external
def name() -> String[32]:
    return "Alexander von Humboldt"


@pure
@external
def addTwo(_initial: uint256) -> uint256:
    return _initial + 2


# ERC 165
@view
@external
def supportsInterface(_interfaceId: Bytes[4]) -> bool:
    # doing this is quite cumbersome in Vyper because of unflexible types

    f_name: bytes32 = method_id("name", output_type=bytes32)
    f_storage: bytes32 = method_id("storage", output_type=bytes32)
    f_addTwo: bytes32 = method_id("addTwo(uint256)", output_type=bytes32)

    f: uint256 = bitwise_xor(
        convert(f_name, uint256),
        convert(f_storage, uint256)
    )
    f = bitwise_xor(f, convert(f_addTwo, uint256))

    return (
        method_id("supportsInterface(bytes4)") == _interfaceId or
        f == convert(_interfaceId, uint256)
    )
