// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

contract FirmaDigital {
    event DocumentoFirmado(address indexed firmante, string hashDocumento, uint256 timestamp);

    function firmarDocumento(string memory hashDocumento) public {
        emit DocumentoFirmado(msg.sender, hashDocumento, block.timestamp);
    }
}