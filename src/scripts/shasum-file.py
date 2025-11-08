import hashlib
import sys

def generar_hash_file(ruta_archivo, algoritmo='sha256'):
    """Genera el hash de un archivo utilizando el algoritmo especificado.

    Args:
        ruta_archivo (str): La ruta del archivo a hashear.
        algoritmo (str): El algoritmo de hash a utilizar ('sha256', 'md5', etc.).

    Returns:
        str: El hash hexadecimal del archivo.
    """
    hash_func = getattr(hashlib, algoritmo)()
    
    with open(ruta_archivo, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)

    return hash_func.hexdigest()

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Uso: python shasum-file.py <ruta_archivo> [algoritmo]")
        sys.exit(1)
    
    ruta = sys.argv[1]
    algoritmo = sys.argv[2] if len(sys.argv) > 2 else 'sha256'
    
    try:
        hash_resultado = generar_hash_file(ruta, algoritmo)
        print(f"{hash_resultado}")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)