import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Image,
  Dimensions,
  SafeAreaView,
  ScrollView,
  BackHandler,  // Add this
  Alert,        // Add this
} from 'react-native';
import { useRouter } from 'expo-router';
import * as SecureStore from 'expo-secure-store';
import { fonts } from './theme';

const { width, height } = Dimensions.get('window');

export default function SixthPage() {
  const router = useRouter();

  const handleDecline = () => {
    // BACKEND: Log decline event and optionally end session before exiting.
    Alert.alert(
      "Exit App",
      "Are you sure you want to exit?",
      [
        {
          text: "Cancel",
          style: "cancel"
        },
        { 
          text: "Exit", 
          onPress: () => BackHandler.exitApp() // BACKEND: flush pending analytics here
        }
      ]
    );
    return true;
  };
  // ... rest of your component

  return (
    <SafeAreaView style={styles.container}>
      
      {/* Menu Button */}
      <TouchableOpacity style={styles.menuButton} onPress={() => router.back()}>
        <View style={styles.menuLine} />
        <View style={styles.menuLine} />
        <View style={styles.menuLine} />
      </TouchableOpacity>

      {/* Doctor Image */}
      <Image
        source={require('../assets/images/imagi.jpg')}
        style={styles.doctorImage}
        resizeMode="contain"
      />

      {/* Terms Box */}
                <View style={styles.termsWrapper}>
                <ScrollView 
                    style={styles.scrollView}
                    contentContainerStyle={styles.scrollContent}
                    showsVerticalScrollIndicator={true}
                >
                    <Text style={styles.termsTitle}>
                    By using Med-ID.AI, you agree to:
                    </Text>

                    <View style={styles.termItem}>
                    <View style={styles.dot} />
                    <Text style={styles.termText}>
                        Allow the app to process and analyze medicine packaging and labels.
                    </Text>
                    </View>

                    <View style={styles.termItem}>
                    <View style={styles.dot} />
                    <Text style={styles.termText}>
                        Accept that the information provided may not always be complete or error-free.
                    </Text>
                    </View>

                    <View style={styles.termItem}>
                    <View style={styles.dot} />
                    <Text style={styles.termText}>
                        Take full responsibility for how you use the app's information.
                    </Text>
                    </View>
                </ScrollView>

                {/* Question moved here but still inside termsWrapper */}
                <Text style={styles.footerQuestion}>
                    Do you agree on using{"\n"}Med-ID.Ai under these terms?
                </Text>
                </View>
      

      {/* Buttons */}
      <View style={styles.buttonRow}>
        <TouchableOpacity style={styles.declineBtn} onPress={handleDecline}>
          <Text style={styles.declineText}>Decline</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.agreeBtn}
          onPress={async () => {
            console.log('Agree button pressed, navigating to SeventhPage');
            try {
              // BACKEND: Record consent accepted and initialize scan session if needed.
              await SecureStore.setItemAsync('disclaimerAccepted', 'true');
              await router.push('SeventhPage');
            } catch (error) {
              console.error('Navigation error:', error);
              Alert.alert('Error', 'Could not open camera. Please try again.');
            }
          }}
        >
          <Text style={styles.agreeText}>Agree & Continue</Text>
        </TouchableOpacity>
      </View>

      {/* Home Indicator */}
      <View style={styles.homeIndicator} />

    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
    alignItems: 'center'
  },

  menuButton: {
    position: 'absolute',
    top: 40,
    left: 36,
    zIndex: 20
  },

  menuLine: {
    width: 28,
    height: 3,
    backgroundColor: '#000',
    marginVertical: 4,
    borderRadius: 3
  },

  doctorImage: {
    width: width * 0.55,
    height: width * 0.55,
    marginTop: 80
  },

 termsWrapper: {
  width: '88%',
  backgroundColor: '#E5E7EB',
  marginTop: -8,
  borderRadius: 25,
  padding: 25,
  paddingBottom: 40, // Less padding at bottom
  maxHeight: '55%', // Adjust based on your needs
},
scrollView: {
  maxHeight: '70%', // This makes the ScrollView take up most of the wrapper
  width: '100%',
},
scrollContent: {
  paddingRight: 10, // Add space for scrollbar
},

  termsTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 20
  },

  termItem: {
    flexDirection: 'row',
    marginBottom: 20
  },

  dot: {
    width: 8,
    height: 8,
    backgroundColor: '#000',
    borderRadius: 4,
    marginRight: 12,
    marginTop: 6
  },

  termText: {
    flex: 1,
    fontSize: 14,
    lineHeight: 20,
    fontFamily: fonts.regular,
  },

  footerQuestion: {
  marginTop: 25,
  fontSize: 18,
  textAlign: 'center',
  paddingHorizontal: 15,
  lineHeight: 24,
  marginBottom: 10,
  fontFamily: fonts.semibold,
},

  buttonRow: {
    width: '88%',
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 30
  },

  declineBtn: {
    width: '48%',
    height: 60,
    backgroundColor: '#E5E7EB',
    borderRadius: 35,
    justifyContent: 'center',
    alignItems: 'center'
  },

  declineText: {
    fontSize: 17,
    fontWeight: '600',
    fontFamily: fonts.semibold,
  },

  agreeBtn: {
    width: '48%',
    height: 60,
    backgroundColor: '#2D9CDB',
    borderRadius: 35,
    justifyContent: 'center',
    alignItems: 'center'
  },

  agreeText: {
    fontSize: 17,
    fontWeight: '700',
    color: '#fff',
    fontFamily: fonts.semibold,
  },

homeIndicator: {
  height: 5,
  width: 134,
  backgroundColor: '#000000',
  borderRadius: 100,
  marginTop: 30,
  marginBottom: 10
}
 
});
