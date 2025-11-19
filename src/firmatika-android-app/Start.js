import React from 'react';
import { View, Text, Image, TextInput, KeyboardAvoidingView, Platform } from 'react-native';
import { TouchableOpacity, StyleSheet } from 'react-native';
import { styles } from './styles';
import { SafeAreaView, SafeAreaProvider } from 'react-native-safe-area-context';

export default function Start({ navigation }) {
    const [text, onChangeText] = React.useState('');
    const [number, onChangeNumber] = React.useState('');
    return (
        // <KeyboardAvoidingView
        //     style={{ flex: 1 }}
        //     behavior={Platform.OS === "ios" ? "padding" : "height"}
        //     keyboardVerticalOffset={0}
        //     backgroundColor="#F5ECE0"
        // >
            <View style={styles.container}>
                {/* Logo  and text */}
                <View style={{ alignItems: 'center', marginTop: 60 }} >
                    <Image source={require('./assets/splash-icon.png')} style={{ width: 128, height: 128 }} />
                    <Text style={[styles.titleH2, { color: '#10c7e7ff',fontSize:28,fontFamily: 'Sans-serif' }]}>FIRMATIKA</Text>
                    <Text style={{fontSize: 14}}>............................................................................</Text>
                    <Text style={styles.titleH2}>Inicie su sesión</Text>
                </View>
                {/* Form */}

                <SafeAreaProvider style={{ alignItems: 'left', marginLeft: 5, marginTop: 60 }}>
                    <SafeAreaView>
                        <View style={{ padding: 10, borderRadius: 10 }}>
                            <Text style={[styles.titleH4, { fontWeight: 'bold', fontSize: 18 }]}>Email</Text>
                            <TextInput
                                style={[styles.input]}
                                onChangeText={onChangeText}
                                placeholder='digite su email'
                                value={text}
                                autoComplete="email"
                                inputMode='email'
                                keyboardType='email-address'
                                textContentType='emailAddress'

                            />
                            <Text style={[styles.titleH4, { fontWeight: 'bold', fontSize: 18 }]}>Contraseña</Text>
                            <TextInput
                                style={styles.input}
                                onChangeText={onChangeNumber}
                                value={number}
                                placeholder="contraseña"
                                secureTextEntry={true}
                                autoComplete='password'
                                inputMode='password'
                                keyboardType='visible-password'
                                textContentType='password'
                            />
                        </View>
                        <View style={{ alignItems: 'center', alignContent: 'center' }}>
                            <Text style={[styles.titleH4]}>No Tienes Cuenta? Registrate aqui</Text>
                        </View>
                    </SafeAreaView>
                </SafeAreaProvider>
                {/* Footer */}
                <View style={{ flex: 1, alignItems: 'center', justifyContent: 'flex-end' }}>
                    <TouchableOpacity
                        style={[styles.buttonMed, { position: 'absolute', alignSelf: 'center', bottom: 65}]}
                        onPress={() => { navigation.replace('Enroll'); }}
                    >
                        <Text style={{ color: '#fff', fontWeight: 'bold' }}>Iniciar sesión</Text>
                    </TouchableOpacity>
                </View>
                {/* Fixed Button */}

            </View>
        // </KeyboardAvoidingView>
    );
}

// const localStyles = StyleSheet.create({

// });