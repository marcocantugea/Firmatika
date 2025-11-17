// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

contract FirmaDigital {
    struct Firma {
        address firmante;
        string nombreDocumento;
        string descripcionDocumento;
        string nombreCompleto;
        bool delegada;
        uint256 timestamp;
    }

    mapping(string => Firma[]) public firmasPorDocumento;
    mapping(string => mapping(address => bool)) public yaFirmo;

    event DocumentoFirmado(address indexed firmante, string nombreCompleto, string nombreDocumento, string descripcionDocumento, string hashDocumento, bool delegada, uint256 timestamp);

    // Firma normal (usuario con su wallet)
    function firmarDocumento(string memory hashDocumento,string memory nombreCompleto,string memory nombreDocumento,string memory descripcionDocumento, bool delegada) public {
        
        firmasPorDocumento[hashDocumento].push(Firma({
            firmante: msg.sender,
            nombreCompleto: nombreCompleto,
            nombreDocumento: nombreDocumento,
            descripcionDocumento: descripcionDocumento,
            delegada: delegada,
            timestamp: block.timestamp
        }));

        yaFirmo[hashDocumento][msg.sender] = true;

        emit DocumentoFirmado(msg.sender, nombreCompleto, nombreDocumento, descripcionDocumento, hashDocumento, delegada, block.timestamp);
    }

    // 🔥 Nueva función: firma delegada explícita
    function firmarDelegada(string memory hashDocumento, string memory nombreCompleto,string memory nombreDocumento,string memory descripcionDocumento, address usuario) public {
        // Aquí Firmatika (msg.sender) firma en nombre de "usuario"

        firmasPorDocumento[hashDocumento].push(Firma({
            firmante: usuario,
            nombreCompleto: nombreCompleto,
            nombreDocumento: nombreDocumento,
            descripcionDocumento: descripcionDocumento,
            delegada: true,
            timestamp: block.timestamp
        }));

        yaFirmo[hashDocumento][usuario] = true;

        emit DocumentoFirmado(usuario, nombreCompleto, nombreDocumento, descripcionDocumento, hashDocumento, true, block.timestamp);
    }

    function obtenerFirmantes(string memory hashDocumento) public view returns (Firma[] memory) {
        return firmasPorDocumento[hashDocumento];
    }
}