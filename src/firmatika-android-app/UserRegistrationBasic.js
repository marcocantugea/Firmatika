import React,{useState} from 'react';
import { 
    View, 
    Text, 
    Image, 
    TextInput, 
    KeyboardAvoidingView, 
    Platform, 
    ActivityIndicator,
    Alert
} from 'react-native';
import { TouchableOpacity, StyleSheet } from 'react-native';
import { styles } from './styles';
import { SafeAreaView, SafeAreaProvider } from 'react-native-safe-area-context';
import { registerUser } from './services/authService';

export default function UserRegistrationBasic({ navigation }) {
   const [nombre, setNombre] = useState('');
    const [apellido, setApellido] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleRegister = () => {
        // Opcional: Validar que los campos no estén vacíos
        if(!nombre || !apellido || !email || !password) {
            Alert.alert("Error", "Por favor llena todos los campos");
            return;
        }

        // Activar el estado de carga
        setIsLoading(true);

        // Simulamos una petición a una API con setTimeout (ej: 2 segundos)
        setTimeout(async () => {
            const userData = { nombre, apellido, email, password };
        
            await registerUser(userData); // Espera la respuesta del servicio

            // 3. Si llega aquí, el registro fue exitoso
            Alert.alert("Éxito", "Usuario registrado correctamente", [
                { text: "OK", onPress: () => navigation.replace('Inicio') }
            ]);
            
            // Al terminar, desactivamos la carga y navegamos
            setIsLoading(false);
            navigation.replace('Inicio'); 
        }, 2000); 
    };
    return (
        <KeyboardAvoidingView
            style={{ flex: 1 }}
            behavior={Platform.OS === "ios" ? "padding" : "height"}
            keyboardVerticalOffset={0}
            backgroundColor="#F5ECE0"
        >
            <View>
                {/* Logo and text */}
                <View style={{ alignItems: 'center', marginTop: 60 }} >
                    <Image source={require('./assets/splash-icon.png')} style={{ width: 64, height: 32 }} />
                    <Text style={[styles.titleH2, { color: '#10c7e7ff', fontSize: 18, fontFamily: 'Sans-serif' }]}>FIRMATIKA</Text>
                    <Text style={{ fontSize: 10 }}>............................................................................</Text>
                    <Text style={styles.titleH2}>Crea tu cuenta</Text>
                </View>
                {/* Formulario */}
                <SafeAreaProvider style={{marginLeft: 5 }}>
                    <SafeAreaView>
                        <View style={{ borderRadius: 10 }}>
                            <Text style={{ marginBottom: 5 }}>Nombre</Text>
                            <TextInput
                                style={styles.input}
                                placeholder="Nombre(s)"
                                value={nombre}
                                onChangeText={setNombre}
                                defaultValue=""
                            />
                            <Text style={{}}>Apellido</Text>
                            <TextInput
                                style={styles.input}
                                placeholder="Apellido(s)"
                                value={apellido}
                                onChangeText={setApellido}
                                defaultValue=""
                            />
                            <Text style={{}}>Email</Text>
                            <TextInput
                                style={styles.input}
                                placeholder="Email"
                                keyboardType="email-address"
                                autoCapitalize="none"
                                defaultValue=""
                                value={email}
                                onChangeText={setEmail}
                            />
                            <Text style={{}}>Contraseña</Text>
                            <TextInput
                                style={styles.input}
                                placeholder="Contraseña"
                                secureTextEntry
                                defaultValue=""
                                value={password}
                                onChangeText={setPassword}
                            />
                            <View style={{ marginTop: 20, alignItems: 'center' }}>
                                <TouchableOpacity
                                    style={[styles.buttonLg, { opacity: isLoading ? 0.7 : 1 }]} // Cambiar opacidad si carga
                                    onPress={handleRegister}
                                    disabled={isLoading} // 5. Deshabilitar botón para evitar doble clic
                                >
                                    {/* 6. Renderizado condicional: Spinner o Texto */}
                                    {isLoading ? (
                                        <ActivityIndicator size="small" color="#fff" />
                                    ) : (
                                        <Text style={{ color: '#fff', fontWeight: 'bold' }}>Registrarse</Text>
                                    )}
                                </TouchableOpacity>
                                <TouchableOpacity
                                    style={[styles.buttonLg, { opacity: isLoading ? 0.7 : 1 }]} // Cambiar opacidad si carga
                                    onPress={() => navigation.replace('Inicio')}
                                    disabled={isLoading} // 5. Deshabilitar botón para evitar doble clic
                                >
                                    {/* 6. Renderizado condicional: Spinner o Texto */}
                                    {isLoading ? (
                                        <ActivityIndicator size="small" color="#fff" />
                                    ) : (
                                        <Text style={{ color: '#fff', fontWeight: 'bold' }}>Iniciar sesión</Text>
                                    )}
                                </TouchableOpacity>
                            </View>
                        </View>
                    </SafeAreaView>
                </SafeAreaProvider>
            </View>
        </KeyboardAvoidingView>
    );
}