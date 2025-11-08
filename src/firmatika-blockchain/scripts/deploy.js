const hre = require("hardhat");

async function main() {
  const FirmaDigital = await hre.ethers.getContractFactory("FirmaDigital");
  const contrato = await FirmaDigital.deploy();
  await contrato.waitForDeployment(); // ← esta línea es clave

  console.log("Contrato desplegado en:", await contrato.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});