import { StatusBar } from 'expo-status-bar';
import { Text, View, Image } from 'react-native';
import { TouchableOpacity } from 'react-native';
import { styles } from './styles';

export default function WelcomeScreen({ navigation }) {
  return (
    <View style={[styles.container, {flexDirection: 'column'}]}>
      
      <View style={{ flex: 2}} />
      <View style={{ flex: 4, alignContent: 'center' , alignItems: 'center'}} >
        <Image source={require('./assets/splash-icon.png')} style={{width: 128, height: 128}} />
        <Text style={{ fontSize: 28, color:'#265161ff' }}>Bienvenido a Firmatika</Text>
        <Text style={{ fontSize: 16, color:'#265161ff', marginTop:10 }}>La mejor app de gestion para tu negocio</Text>
        <Text style={{ fontSize: 16, color:'#265161ff', marginTop:10, textAlign: 'center' }}>Firma digitalmente tus documentos con seguridad y utilizando tecnología blockchain</Text>
        <Text>{'\n'}</Text>
        <TouchableOpacity
          style={styles.buttonLg}
          onPress={() => { navigation.replace('Inicio');}}
        >
          <Text style={{ color: '#fff', fontWeight: 'bold' }}>Empezar</Text>
        </TouchableOpacity>
      </View>
      <View style={{ flex: 1}} />
      <StatusBar style="auto" />
    </View>
  );
}