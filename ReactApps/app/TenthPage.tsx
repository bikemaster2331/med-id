import React from 'react';
import { View, Text, StyleSheet, ScrollView, Image, TouchableOpacity } from 'react-native';
import { fonts } from './theme';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function TenthPage() {
  const { name, photoUri } = useLocalSearchParams<{ name?: string; photoUri?: string }>();
  const router = useRouter();

  return (
    <View style={styles.container}>
      <View style={styles.topBar}>
        <TouchableOpacity onPress={() => router.back()} style={styles.iconBtn}>
          <Ionicons name="arrow-back" size={22} color="#000" />
        </TouchableOpacity>
        <Text style={styles.title}>Medicine Details</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView contentContainerStyle={{ paddingBottom: 28 }}>
        {photoUri ? (
          <Image source={{ uri: photoUri }} style={styles.image} resizeMode="contain" />
        ) : null}

        <View style={styles.card}>
          <Text style={styles.medName}>{name || 'Medicine name'}</Text>

          {/* BACKEND: Populate all fields below from the API response */}
          <Text style={styles.sectionLabel}>Category</Text>
          <Text style={styles.valueText}>Analgesic (pain reliever), Antipyretic (fever reducer)</Text>

          <Text style={styles.sectionLabel}>Dose</Text>
          <Text style={styles.valueText}>Adults: 325–500 mg. Children: weight-based.</Text>

          <Text style={styles.sectionLabel}>Available Forms</Text>
          <Text style={styles.valueText}>Tablet, syrup, suppository</Text>

          <Text style={styles.sectionLabel}>Ingredients</Text>
          <Text style={styles.valueText}>Paracetamol (Acetaminophen)</Text>

          <Text style={styles.sectionLabel}>Expiry Date</Text>
          <Text style={styles.valueText}>—</Text>

          <Text style={styles.sectionLabel}>Brand Name</Text>
          <Text style={styles.valueText}>—</Text>

          <Text style={styles.sectionLabel}>Description</Text>
          <Text style={styles.valueText}>
            Helps relieve mild to moderate pain and reduces fever. (Replace with backend data.)
          </Text>

          <TouchableOpacity
            style={[styles.primaryBtn, { marginTop: 18 }]}
            onPress={() => {
              // BACKEND: finalization/analytics can be triggered here
              router.push('/EleventhPage');
            }}
          >
            <Text style={styles.btnText}>Finish</Text>
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
  image: { width: '100%', height: 220, borderRadius: 12, backgroundColor: '#fafafa' },
  card: { backgroundColor: '#fff', borderRadius: 20, padding: 16, marginTop: 16, borderWidth: 1, borderColor: '#eee' },
  medName: { fontSize: 18, fontWeight: '700', marginBottom: 8, fontFamily: fonts.semibold },
  sectionLabel: { fontSize: 14, fontWeight: '600', marginTop: 10, marginBottom: 6, color: '#444', fontFamily: fonts.semibold },
  valueText: { fontSize: 14, lineHeight: 20, color: '#222', fontFamily: fonts.regular },
  primaryBtn: { height: 50, borderRadius: 25, backgroundColor: '#2D9CDB', alignItems: 'center', justifyContent: 'center' },
  btnText: { color: '#fff', fontSize: 16, fontWeight: '600', fontFamily: fonts.semibold },
});
