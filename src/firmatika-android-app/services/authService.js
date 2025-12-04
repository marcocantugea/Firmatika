import { API_BASE_URL } from '../servicesConfig';
import { VerificationRequest } from '../Models/VerificationRequest';
import { UserCreationRequest } from '../Models/UserCreationRequest';
/**
 * Función para registrar un nuevo usuario en la API.
 * @param {object} userData - Datos del usuario (nombre, apellido, email, password).
 * @returns {Promise<object>} Retorna los datos de éxito o lanza un error.
 */
export const registerUser = async (UserCreationRequest) => {
    const url = `${API_BASE_URL}/registro`;

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(UserCreationRequest),
        });

        // 1. Manejo de Errores del Servidor (Códigos 4xx o 5xx)
        if (!response.ok) {
            // Intenta leer el mensaje de error del cuerpo de la respuesta
            const errorData = await response.json().catch(() => ({ message: 'Error desconocido del servidor.' }));
            
            // Lanzamos un error que el componente de React Native capturará.
            throw new Error(errorData.message || 'Fallo en la conexión o datos inválidos.');
        }

        // 2. Retorna los datos de éxito
        return response.json(); 

    } catch (error) {
        // Manejo de errores de red (Ej. No hay internet)
        throw new Error("No se pudo conectar con el servidor. " + error.message);
    }
};

export const verifyUser = async (VerificationRequest) => {
    const url = `${API_BASE_URL}/verificar`;

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ message: 'Error desconocido del servidor.' }));
            throw new Error(errorData.message || 'Fallo en la conexión o datos inválidos.');
        }

        return response.json(); 

    } catch (error) {
        throw new Error("No se pudo conectar con el servidor. " + error.message);
    }
};