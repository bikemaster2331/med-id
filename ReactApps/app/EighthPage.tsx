import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { fonts } from './theme';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function EighthPage() {
  const { photoUri } = useLocalSearchParams<{ photoUri: string }>();
  const router = useRouter();
  // BACKEND: This is the photo confirmation step. Nom           k,llllll upload yet.
  // When user taps Proceed, navigate to NinthPage where the backend will receive
  // the image and return parsed medicine data.
  
  return (
    <View style={styles.container}>
      <View style={styles.topBar}>
        <TouchableOpacity
          onPress={() => {
            // Retake: go back to camera
            if (router && typeof router.back === 'function') router.back();
            else router.push('/SeventhPage');
          }}
          style={styles.iconBtn}
        >
          <Ionicons name="arrow-back" size={22} color="#000" />
        </TouchableOpacity>
        <Text style={styles.title}>Photo Preview</Text>
        <View style={{ width: 40 }} />
      </View>
      {photoUri ? (
        <Image 
          source={{ uri: photoUri as string }} 
          style={styles.image} 
          resizeMode="contain"
        />
      ) : (
        <Text>No photo available</Text>
      )}
      <View style={styles.actions}>
        <TouchableOpacity
          style={[styles.btn, styles.retakeBtn]}
          onPress={() => {
            // Retake: back to camera
            if (router && typeof router.back === 'function') router.back();
            else router.push('/SeventhPage');
          }}
        >
          <Text style={[styles.btnText, { color: '#000' }]}>Retake</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.btn, styles.proceedBtn]}
          onPress={() => {
            // BACKEND: Actual upload & processing should occur in NinthPage.
            router.push({ pathname: '/NinthPage', params: { photoUri: (photoUri as string) || '' } });
          }}
        >
          <Text style={styles.btnText}>Proceed</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 24,
    paddingHorizontal: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 0,
    fontFamily: fonts.display,
  },
  topBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  iconBtn: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#f1f1f3',
    alignItems: 'center',
    justifyContent: 'center',
  },
  image: {
    width: '100%',
    height: 380,
    borderRadius: 10,
  },
  actions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 24,
  },
  btn: {
    flex: 1,
    height: 52,
    borderRadius: 26,
    alignItems: 'center',
    justifyContent: 'center',
  },
  retakeBtn: {
    backgroundColor: '#eaeaea',
    marginRight: 10,
  },
  proceedBtn: {
    backgroundColor: '#2D9CDB',
    marginLeft: 10,
  },
  btnText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    fontFamily: fonts.semibold,
  },
});
