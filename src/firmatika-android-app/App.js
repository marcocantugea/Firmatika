import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import Start from './Start'; // Asegúrate de que la ruta sea correcta
import WelcomeScreen from './WelcomeScreen';


const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Bienvenido" component={WelcomeScreen} options={{headerShown:false}} />
        <Stack.Screen name="Inicio" component={Start} options={{headerShown:false}} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}