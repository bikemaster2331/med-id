import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { fonts } from './theme';
import { useRouter } from 'expo-router';
import * as SecureStore from 'expo-secure-store';

export default function StartPage() {
  const router = useRouter();
  
  const handleGetStarted = async () => {
    // BACKEND: Optionally initialize session, fetch remote config, or log onboarding start.
    try {
      const accepted = await SecureStore.getItemAsync('disclaimerAccepted');
      if (accepted === 'true') {
        router.push('/SeventhPage');
      } else {
        router.push('/FifthPage');
      }
    } catch (e) {
      router.push('/FifthPage');
    }
  };
  
  return (
    <View style={styles.container}>
      <View style={styles.logoBox}>
        <View style={styles.logoInner}>
          <Text style={styles.logoText}>M</Text>
        </View>
      </View>

      <Text style={styles.title}>MEDICAL ID</Text>
      <Text style={styles.subtitle}>AI–POWERED MEDICINE ID</Text>

      <TouchableOpacity
        style={styles.btn}
        onPress={handleGetStarted}
      >
        <Text style={styles.btnText}>Get Started</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
  },
  logoBox: {
    width: 280,
    height: 280,
    backgroundColor: "#000",
    padding: 20,
    marginTop: 140,
  },
  logoInner: {
    flex: 1,
    backgroundColor: "#fff",
    justifyContent: "center",
    alignItems: "center",
  },
  logoText: {
    fontSize: 200,
    fontWeight: "900",
    color: "#000",
  },
  title: {
    marginTop: 40,
    fontSize: 40,
    fontWeight: "bold",
    color: "#000",
    fontFamily: fonts.display,
  },
  subtitle: {
    fontSize: 18,
    color: "gray",
    marginTop: 8,
    fontFamily: fonts.regular,
  },
  btn: {
    position: "absolute",
    bottom: 120,
    width: 300,
    height: 60,
    borderRadius: 30,
    backgroundColor: "#e5e5e7",
    justifyContent: "center",
    alignItems: "center",
  },
  btnText: {
    fontSize: 18,
    fontWeight: "600",
    color: "#000",
    fontFamily: fonts.semibold,
  },
});
