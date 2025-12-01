import React, { useEffect } from 'react';
import { 
  View, 
  Text, 
  TouchableOpacity, 
  StyleSheet, 
  Image, 
  Dimensions,
  SafeAreaView,
  Platform,
  ScrollView,
  StyleProp,
  ViewStyle,
  TextStyle,
} from 'react-native';
import { useRouter } from 'expo-router';
import * as SecureStore from 'expo-secure-store';
import { fonts } from './theme';

const { width, height } = Dimensions.get('window');

// Use a solid color background instead of the image
const warningIcon = { uri: 'https://c.animaapp.com/mgk7zbe6pTjD2o/img/triangle-warning--1-.png' };

// Style for the background container
const backgroundStyle = {
  backgroundColor: '#f0f4f8', // Light blue-gray background
  flex: 1,
};

export default function FifthPage() {
  const router = useRouter();

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const accepted = await SecureStore.getItemAsync('disclaimerAccepted');
        if (mounted && accepted === 'true') {
          router.replace('/SeventhPage');
        }
      } catch {}
    })();
    return () => { mounted = false; };
  }, [router]);

  const handleUnderstand = () => {
    // BACKEND: Record that user acknowledged the disclaimer (analytics/consent).
    router.push('/SixthPage');
  };

  // Images are now defined at the top of the file

  // Apply responsive styles based on screen size
  const isSmallDevice = width < 420;
  const isVerySmallDevice = width < 340;

  const getResponsiveStyles = () => {
    const cardStyles: Array<StyleProp<ViewStyle>> = [styles.card];
    const titleStyles: Array<StyleProp<TextStyle>> = [styles.title];
    const textStyles: Array<StyleProp<TextStyle>> = [styles.text];
    const buttonStyles: Array<StyleProp<ViewStyle>> = [styles.button];
    const buttonTextStyles: Array<StyleProp<TextStyle>> = [styles.buttonText];

    if (isSmallDevice) {
      cardStyles.push({
        marginTop: 110,
        padding: 28,
        borderRadius: 28,
      });
      titleStyles.push({
        fontSize: 28,
      });
      textStyles.push({
        fontSize: 15,
      });
      buttonStyles.push({
        width: 180,
        height: 54,
      });
      buttonTextStyles.push({
        fontSize: 18,
      });
    }

    if (isVerySmallDevice) {
      cardStyles.push({
        marginTop: 90,
        padding: 22,
      });
    }

    return {
      card: StyleSheet.flatten(cardStyles),
      title: StyleSheet.flatten(titleStyles),
      text: StyleSheet.flatten(textStyles),
      button: StyleSheet.flatten(buttonStyles),
      buttonText: StyleSheet.flatten(buttonTextStyles),
    };
  };

  const responsiveStyles = getResponsiveStyles();

  return (
    <View style={[styles.container, backgroundStyle]}>
      {/* Solid color background */}
      <View style={[styles.backgroundImage, { backgroundColor: '#e1e8f0' }]} />
      
      {/* Semi-transparent overlay */}
      <View style={[styles.dimOverlay, { backgroundColor: 'rgba(0, 0, 0, 0.4)' }]} />

      {/* Content */}
      <SafeAreaView style={styles.safeArea}>
        <ScrollView contentContainerStyle={styles.scrollView}>
          <View style={responsiveStyles.card}>
            <Image 
              source={warningIcon} 
              style={styles.warningIcon} 
              resizeMode="contain"
            />
            <Text style={responsiveStyles.title}>Disclaimer</Text>
            
            <Text style={responsiveStyles.text}>
              Med-ID.AI is designed to help identify medicines and provide general information.
              It does not replace professional medical advice, diagnosis, or treatment.
              Always consult your doctor or pharmacist before making any health decisions.
            </Text>

            <TouchableOpacity 
              style={responsiveStyles.button}
              onPress={handleUnderstand}
            >
              <Text style={responsiveStyles.buttonText}>I Understand</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f6f7f8',
  },
  backgroundImage: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    width: '100%',
    height: '100%',
    zIndex: -1,
  },
  dimOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(90, 90, 90, 0.55)',
  },
  safeArea: {
    flex: 1,
  },
  scrollView: {
    flexGrow: 1,
    justifyContent: 'center',
    paddingVertical: 20,
  },
  card: {
    backgroundColor: 'rgba(255, 255, 255, 0.85)', // Semi-transparent white background
    borderWidth: 2,
    borderColor: 'rgba(0, 0, 0, 0.1)', // Lighter border
    borderRadius: 40,
    marginHorizontal: 20,
    marginTop: 20,
    padding: 30,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 12 },
    shadowOpacity: 0.15,
    shadowRadius: 30,
    elevation: 5,
  },
  warningIcon: {
    width: 92,
    height: 92,
    marginBottom: 20,
  },
  title: {
    fontSize: 36,
    fontWeight: '700',
    marginBottom: 16,
    color: '#000',
    textAlign: 'center',
    fontFamily: fonts.display,
  },
  text: {
    fontSize: 16,
    color: '#111',
    lineHeight: 24,
    marginBottom: 30,
    textAlign: 'center',
    fontFamily: fonts.regular,
  },
  button: {
    width: 220,
    height: 64,
    borderRadius: 32,
    backgroundColor: '#2d9cdb',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#2d9cdb',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.25,
    shadowRadius: 18,
    elevation: 5,
  },
  buttonText: {
    color: '#fff',
    fontSize: 20,
    fontWeight: '700',
    fontFamily: fonts.semibold,
  },
});
