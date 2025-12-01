import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity, ScrollView, Alert, BackHandler } from 'react-native';
import { fonts } from './theme';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function EleventhPage() {
  const router = useRouter();
  const handleExit = () => {
    Alert.alert(
      'Exit App',
      'Are you sure you want to exit?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Exit', onPress: () => BackHandler.exitApp() }
      ]
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.topBar}>
        <TouchableOpacity onPress={() => router.back()} style={styles.iconBtn}>
          <Ionicons name="arrow-back" size={22} color="#000" />
        </TouchableOpacity>
        <Text style={styles.title}>Scan Completed</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView contentContainerStyle={{ paddingBottom: 28 }}>
        <View style={styles.tipBubble}>
          <View style={styles.tipCircle}>
            <Ionicons name="happy-outline" size={42} color="#2D9CDB" />
          </View>
          <Text style={styles.tipTitle}>Always wear a face mask</Text>
          <Text style={styles.tipSub}>should never go out without a face mask always remember to put it on</Text>
          <View style={styles.cloudRow}>
            <Ionicons name="cloud-outline" size={22} color="#ffffff" style={{ opacity: 0.9 }} />
            <Ionicons name="cloud-outline" size={16} color="#ffffff" style={{ marginLeft: 8, opacity: 0.7 }} />
            <Ionicons name="cloud-outline" size={12} color="#ffffff" style={{ marginLeft: 6, opacity: 0.6 }} />
          </View>
        </View>

        <View style={styles.card}>
          <View style={styles.logoBox}>
            <Text style={styles.logoM}>M</Text>
          </View>
          <Text style={styles.brandTitle}>MEDICAL ID</Text>
          <Text style={styles.brandSub}>AI—POWERED MEDICINE ID</Text>
          <Text style={styles.scanTitle}>Scan Completed</Text>

          <View style={styles.confettiA} />
          <View style={styles.confettiB} />
          <View style={styles.confettiC} />
          <View style={styles.confettiD} />
          <View style={styles.confettiE} />

          <View style={styles.pill}>
            <Text style={styles.pillText}>THANK YOU FOR USING MED-ID!</Text>
          </View>
          <View style={styles.pill}>
            <Text style={styles.pillText}>Discover Medicine Information with Med-ID.AI</Text>
          </View>
          <Text style={styles.note}>Stay safe, stay informed. Med-ID is always here to help</Text>
        </View>

        <View style={styles.actions}>
          <TouchableOpacity
            style={[styles.btn, styles.primaryBtn]}
            onPress={() => {
              // BACKEND: Optionally notify backend that session completed.
              router.replace('/SeventhPage'); // Scan another
            }}
          >
            <Text style={styles.btnText}>Scan another medicine</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.btn, styles.secondaryBtn]}
            onPress={() => {
              // BACKEND: Optionally record navigation to home.
              handleExit();
            }}
          >
            <Text style={[styles.btnText, { color: '#000' }]}>Exit</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', paddingTop: 24, paddingHorizontal: 20 },
  topBar: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 },
  title: { fontSize: 22, fontWeight: '700', fontFamily: fonts.display },
  iconBtn: { width: 40, height: 40, borderRadius: 20, backgroundColor: '#f1f1f3', alignItems: 'center', justifyContent: 'center' },
  tipBubble: {
    backgroundColor: '#5AA6FF',
    borderRadius: 24,
    padding: 16,
    alignItems: 'center',
    marginBottom: 16,
  },
  tipCircle: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: '#EAF3FF',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 10,
  },
  tipTitle: { color: '#fff', fontSize: 14, fontWeight: '700', textAlign: 'center', fontFamily: fonts.semibold },
  tipSub: { color: '#f0f7ff', fontSize: 12, textAlign: 'center', marginTop: 4, fontFamily: fonts.regular },
  cloudRow: { flexDirection: 'row', marginTop: 8 },

  card: {
    backgroundColor: '#ffffff',
    borderRadius: 28,
    paddingVertical: 22,
    paddingHorizontal: 18,
    borderWidth: 1,
    borderColor: '#ECECEC',
    alignItems: 'center',
  },
  logoBox: {
    width: 84,
    height: 84,
    borderRadius: 12,
    borderWidth: 3,
    borderColor: '#000',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 10,
  },
  logoM: { fontSize: 44, fontWeight: '900', color: '#000', fontFamily: fonts.display },
  brandTitle: { fontSize: 16, fontWeight: '800', marginTop: 2, fontFamily: fonts.display },
  brandSub: { fontSize: 12, color: '#555', marginBottom: 12, fontFamily: fonts.regular },
  scanTitle: { fontSize: 18, fontWeight: '800', marginBottom: 8, fontFamily: fonts.display },
  pill: {
    backgroundColor: '#EDEDED',
    paddingVertical: 10,
    paddingHorizontal: 14,
    borderRadius: 14,
    marginBottom: 8,
  },
  pillText: { fontSize: 12, color: '#333', fontFamily: fonts.semibold },
  note: { fontSize: 14, color: '#333', textAlign: 'center', marginTop: 6, fontFamily: fonts.regular },

  confettiA: { position: 'absolute', top: 28, left: 22, width: 8, height: 8, borderRadius: 4, backgroundColor: '#FF7A59' },
  confettiB: { position: 'absolute', top: 36, right: 28, width: 6, height: 6, borderRadius: 3, backgroundColor: '#6C63FF' },
  confettiC: { position: 'absolute', top: 72, right: 54, width: 10, height: 10, borderRadius: 5, backgroundColor: '#00B894' },
  confettiD: { position: 'absolute', top: 88, left: 42, width: 6, height: 6, borderRadius: 3, backgroundColor: '#FFB300' },
  confettiE: { position: 'absolute', top: 60, left: 120, width: 4, height: 4, borderRadius: 2, backgroundColor: '#E84393' },

  actions: { marginTop: 20 },
  btn: { height: 54, borderRadius: 27, alignItems: 'center', justifyContent: 'center', marginBottom: 12 },
  primaryBtn: { backgroundColor: '#2D9CDB' },
  secondaryBtn: { backgroundColor: '#eaeaea' },
  btnText: { color: '#fff', fontSize: 16, fontWeight: '600', fontFamily: fonts.semibold },
})
