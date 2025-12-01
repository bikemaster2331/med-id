// In _layout.tsx
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function RootLayout() {
  return (
    <>
      <StatusBar style="dark" />
      <Stack 
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: '#fff' },
          animation: 'slide_from_right',
          gestureEnabled: true,
        }}
      >
        <Stack.Screen name="index" />
        <Stack.Screen name="StartPage" />
        <Stack.Screen name="FifthPage" />
        <Stack.Screen name="SixthPage" />
        <Stack.Screen name="SeventhPage" />
        <Stack.Screen name="EighthPage" />
        <Stack.Screen name="NinthPage" />
        <Stack.Screen name="TenthPage" />
        <Stack.Screen name="EleventhPage" />
      </Stack>
    </>
  );
}