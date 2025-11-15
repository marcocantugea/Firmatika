// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

contract FirmaDigital {
    struct Firma {
        address firmante;
        bool delegada;
        uint256 timestamp;
    }

    mapping(string => Firma[]) public firmasPorDocumento;
    mapping(string => mapping(address => bool)) public yaFirmo;

    event DocumentoFirmado(address indexed firmante, string hashDocumento, bool delegada, uint256 timestamp);

    function firmarDocumento(string memory hashDocumento, bool delegada) public {
        require(!yaFirmo[hashDocumento][msg.sender], "Ya has firmado este documento");

        firmasPorDocumento[hashDocumento].push(Firma({
            firmante: msg.sender,
            delegada: delegada,
            timestamp: block.timestamp
        }));

        yaFirmo[hashDocumento][msg.sender] = true;

        emit DocumentoFirmado(msg.sender, hashDocumento, delegada, block.timestamp);
    }

    function obtenerFirmantes(string memory hashDocumento) public view returns (Firma[] memory) {
        return firmasPorDocumento[hashDocumento];
    }
}