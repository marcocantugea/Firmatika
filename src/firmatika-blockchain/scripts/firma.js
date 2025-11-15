const hre = require("hardhat");

async function main() {
  const contrato = await hre.ethers.getContractAt("FirmaDigital", "0xCbC77A793F16f6127772Ad16DbBB8a29a9Ec20CB");
  const tx = await contrato.firmarDocumento("4020d4be5ce3507361a4aaffda66628dbede83779e208babea3172b66f00b711",true);
  await tx.wait();
  console.log("Documento firmado en la transacción:", tx.hash);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});