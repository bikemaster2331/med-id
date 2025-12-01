import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, Image, ActivityIndicator, ScrollView, TouchableOpacity } from 'react-native';
import { fonts } from './theme';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function NinthPage() {
  const { photoUri } = useLocalSearchParams<{ photoUri: string }>();
  const router = useRouter();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [summary, setSummary] = useState<{ name: string; description: string } | null>(null);

  useEffect(() => {
    let mounted = true;
    async function run() {
      try {
        // BACKEND: Upload the image (photoUri) to your API here and parse medicine data.
        // Example:
        // const res = await fetch(API_URL + '/scan', { method: 'POST', body: formDataWith(photoUri) })
        // const data = await res.json(); setSummary(data.summary)
        // For now we simulate a short delay and mock data.
        await new Promise(r => setTimeout(r, 800));
        if (!mounted) return;
        setSummary({
          name: 'PARACETAMOL 500 mg TABLET',
          description:
            'Helps relieve mild to moderate pain and reduces fever. Commonly used for headaches, toothaches, muscle aches, and other discomforts.',
        });
      } catch (e: any) {
        if (!mounted) return;
        setError('Failed to process image. Please try again.');
      } finally {
        if (mounted) setLoading(false);
      }
    }
    run();
    return () => {
      mounted = false;
    };
  }, [photoUri]);

  return (
    <View style={styles.container}>
      <View style={styles.topBar}>
        <TouchableOpacity onPress={() => router.back()} style={styles.iconBtn}>
          <Ionicons name="arrow-back" size={22} color="#000" />
        </TouchableOpacity>
        <Text style={styles.title}>Scan Result</Text>
        <View style={{ width: 40 }} />
      </View>

      {loading && (
        <View style={styles.centerBox}>
          <ActivityIndicator size="large" color="#2D9CDB" />
          <Text style={styles.loadingText}>Processing scan…</Text>
        </View>
      )}

      {!loading && error && (
        <View style={styles.centerBox}>
          <Text style={styles.errorText}>{error}</Text>
          <TouchableOpacity style={styles.primaryBtn} onPress={() => router.replace({ pathname: '/NinthPage', params: { photoUri: (photoUri as string) || '' } })}>
            <Text style={styles.btnText}>Retry</Text>
          </TouchableOpacity>
        </View>
      )}

      {!loading && !error && (
        <ScrollView contentContainerStyle={{ paddingBottom: 24 }}>
          {photoUri ? (
            <Image source={{ uri: photoUri as string }} style={styles.image} resizeMode="contain" />
          ) : null}

          {/* Summary Card (Pre-details) */}
          <View style={styles.card}>
            <Text style={styles.medName}>{summary?.name || 'Medicine name'}</Text>
            <Text style={styles.sectionLabel}>Description</Text>
            <Text style={styles.description}>{summary?.description || '—'}</Text>

            <TouchableOpacity
              style={[styles.primaryBtn, { marginTop: 16 }]}
              onPress={() => {
                // BACKEND: Pass full API result to TenthPage (either via global store or params)
                router.push({ pathname: '/TenthPage', params: { name: summary?.name || '', photoUri: (photoUri as string) || '' } });
              }}
            >
              <Text style={styles.btnText}>See full details</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#ffffffff', paddingTop: 54, paddingHorizontal: 20 },
  topBar: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 },
  title: { fontSize: 22, fontWeight: '700', fontFamily: fonts.display },
  iconBtn: { width: 40, height: 40, borderRadius: 20, backgroundColor: '#f1f1f3', alignItems: 'center', justifyContent: 'center' },
  centerBox: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  loadingText: { marginTop: 12, color: '#333', fontFamily: fonts.regular },
  errorText: { color: '#d00', marginBottom: 12, textAlign: 'center', fontFamily: fonts.regular },
  image: { width: '100%', height: 240, borderRadius: 12, backgroundColor: '#fafafa' },
  card: { backgroundColor: '#fff', borderRadius: 20, padding: 50, marginTop: 46, borderWidth: 2, borderColor: '#eee' },
  medName: { fontSize: 20, fontWeight: '700', marginBottom: 8, fontFamily: fonts.semibold },
  sectionLabel: { fontSize: 14, fontWeight: '600', marginTop: 8, marginBottom: 6, color: '#444', fontFamily: fonts.semibold },
  description: { fontSize: 18, lineHeight: 20, color: '#222', fontFamily: fonts.regular },
  primaryBtn: { height: 50, borderRadius: 25, backgroundColor: '#2D9CDB', alignItems: 'center', justifyContent: 'center' },
  btnText: { color: '#fff', fontSize: 20, fontWeight: '600', fontFamily: fonts.semibold },
})
