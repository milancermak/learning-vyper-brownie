# @version ^0.2.0

# https://eips.ethereum.org/EIPS/eip-165
interface IERC165:
    def supportsInterface(interfaceId: Bytes[4]) -> bool: view
