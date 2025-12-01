import React, { useState, useRef, useEffect, useCallback } from 'react';
import { 
  StyleSheet, 
  View, 
  Text, 
  TouchableOpacity, 
  Image,
  Dimensions,
  Animated,
  Platform,
  ActivityIndicator,
  Alert,
  Linking,
  StyleProp,
  ViewStyle
} from 'react-native';
import { Camera, CameraType, CameraView } from 'expo-camera';
import { useRouter, useFocusEffect } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import * as MediaLibrary from 'expo-media-library';
import { BackHandler } from 'react-native';

const { width, height } = Dimensions.get('window');

const CameraFrame = ({ style }: { style?: StyleProp<ViewStyle> }) => (
  <View style={[styles.frameContainer, style]}>
    <View style={[styles.frameCorner, styles.frameCornerTopLeft]} />
    <View style={[styles.frameCorner, styles.frameCornerTopRight]} />
    <View style={[styles.frameCorner, styles.frameCornerBottomLeft]} />
    <View style={[styles.frameCorner, styles.frameCornerBottomRight]} />
  </View>
);

export default function SeventhPage() {
  // Initialize router from expo-router
  const router = useRouter();
  
  const [isReady, setIsReady] = useState(false);
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [cameraType, setCameraType] = useState<CameraType>('back');

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [cameraReady, setCameraReady] = useState(false);
  const cameraRef = useRef<any>(null);

  const fadeAnim = useRef(new Animated.Value(0)).current;

  // Initialize component
  useEffect(() => {
    let isMounted = true;
    
    const initialize = async () => {
      try {
        console.log('Initializing SeventhPage...');
        
        // Request camera permissions
        // BACKEND: Optionally log permission requests/results for analytics.
        const { status } = await Camera.requestCameraPermissionsAsync();
        if (isMounted) {
          setHasPermission(status === 'granted');
          if (status !== 'granted') {
            setError('Camera permission is required to use this feature.');
          }
          setIsReady(true);
        }
      } catch (err) {
        console.error('Initialization error:', err);
        if (isMounted) {
          setError('Failed to initialize camera. Please restart the app.');
          setIsReady(true);
        }
      }
    };

    initialize();
    
    return () => {
      isMounted = false;
    };
  }, []);

  // Handle back navigation with maximum safety
  const handleBack = useCallback(() => {
    console.log('handleBack called');
    // BACKEND: Track user navigating back from camera (cancel scan).
    
    if (router && typeof router.back === 'function') {
      console.log('Using router.back()');
      router.back();
      return;
    }
    
    if (router && typeof router.push === 'function') {
      console.log('Using router.push("..")');
      router.push('..');
      return;
    }
    
    if (typeof window !== 'undefined' && window.history) {
      console.log('Using window.history.back()');
      window.history.back();
      return;
    }
    
    console.warn('No navigation method available');
  }, [router]);

  // Handle hardware back button on Android
  useFocusEffect(
    useCallback(() => {
      if (!isReady) return;
      
      console.log('useFocusEffect triggered');
      
      if (Platform.OS === 'android') {
        const onBackPress = () => {
          console.log('Android back button pressed');
          handleBack();
          return true; // Prevent default back behavior
        };
        
        const backHandler = BackHandler.addEventListener(
          'hardwareBackPress',
          onBackPress
        );
        
        return () => {
          console.log('Cleaning up back handler');
          backHandler.remove();
        };
      }
    }, [handleBack, isReady])
  );

  // Animation for the camera overlay
  useEffect(() => {
    const animation = Animated.loop(
      Animated.sequence([
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(fadeAnim, {
          toValue: 0.3,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    );
    
    animation.start();
    return () => animation.stop();
  }, []);

  const openSettings = async () => {
    if (Platform.OS === 'ios') {
      await Linking.openURL('app-settings:');
    } else {
      await Linking.openSettings();
    }
  };

  // Allow selecting an image from the gallery (Android/iOS)
  const pickFromGallery = async () => {
    try {
      setIsLoading(true);
      const perm = await ImagePicker.requestMediaLibraryPermissionsAsync();
      if (perm.status !== 'granted') {
        Alert.alert('Permission required', 'Allow photo access to pick an image.');
        return;
      }
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: false,
        quality: 0.8,
      });
      if (!result.canceled && result.assets && result.assets.length > 0) {
        const uri = result.assets[0].uri;
        if (router?.push) {
          router.push({ pathname: '/EighthPage', params: { photoUri: uri } });
        } else if (typeof window !== 'undefined') {
          window.location.href = `/EighthPage?photoUri=${encodeURIComponent(uri)}`;
        }
      }
    } catch (e) {
      console.error('Image pick error:', e);
      Alert.alert('Error', 'Failed to pick image. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const takePicture = async () => {
    if (!cameraRef.current) {
      console.log('Camera ref is not ready');
      setError('Camera is not ready. Please try again.');
      return;
    }

    try {
      console.log('Attempting to take picture...');
      setIsLoading(true);
      // BACKEND: If you want to upload immediately after capture, you can
      // move the upload here. In this flow, we navigate to EighthPage for
      // preview, then perform the upload and parsing in NinthPage.
      const anyRef = cameraRef.current as any;
      let photo: any = null;
      if (typeof anyRef?.takePictureAsync === 'function') {
        photo = await anyRef.takePictureAsync({
          quality: 0.8,
          base64: true,
          skipProcessing: true,
          exif: false,
        });
      } else if (typeof anyRef?.takePicture === 'function') {
        photo = await anyRef.takePicture({ quality: 0.8 });
      } else {
        throw new Error('CameraView ref does not support taking pictures');
      }
      
      console.log('Picture taken successfully:', photo.uri);
      
      // Save to media library
      try {
        await MediaLibrary.saveToLibraryAsync(photo.uri);
        console.log('Photo saved to library');
      } catch (saveError) {
        console.warn('Failed to save photo to library:', saveError);
      }
      
      // Navigate to EighthPage with the photo data
      if (router?.push) {
        router.push({
          pathname: '/EighthPage',
          params: { photoUri: photo.uri }
        });
      } else if (typeof window !== 'undefined') {
        window.location.href = `/EighthPage?photoUri=${encodeURIComponent(photo.uri)}`;
      }
      
    } catch (error) {
      console.error('Error taking picture:', error);
      setError('Failed to take picture. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleRetry = () => {
    setError(null);
    setHasPermission(null);
  };

  const toggleCameraType = () => {
    setCameraType((current: CameraType) => 
      (current === 'back' ? 'front' : 'back')
    );
  };

  // Show loading state or router error
  if (!isReady || hasPermission === null) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#0000ff" />
        <Text style={styles.loadingText}>Preparing camera...</Text>
      </View>
    );
  }
  
  // Show error or permission denied state
  if (hasPermission === false || error) {
    return (
      <View style={styles.errorContainer}>
        <Ionicons name="warning" size={64} color="#ff3b30" style={styles.errorIcon} />
        <Text style={styles.errorText}>
          {error || 'Camera permission is required to use this feature.'}
        </Text>
        <TouchableOpacity 
          style={styles.retryButton}
          onPress={openSettings}
        >
          <Text style={styles.retryText}>Open Settings</Text>
        </TouchableOpacity>
        <TouchableOpacity 
          style={[styles.retryButton, { backgroundColor: '#007AFF' }]}
          onPress={handleRetry}
        >
          <Text style={styles.retryText}>Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <CameraView
        style={styles.camera}
        facing={cameraType}
        ref={cameraRef}
        onCameraReady={() => {
          console.log('Camera is ready');
          setCameraReady(true);
        }}
      >
        <View style={styles.overlay}>
          <Animated.View 
            style={[styles.overlayTop, { opacity: fadeAnim }]} 
          />
          
          <CameraFrame />

          <Animated.View 
            style={[styles.overlayBottom, { opacity: fadeAnim }]} 
          />
        </View>
      </CameraView>

      <View style={styles.controls}>
        <View style={styles.controlsGroup}>
          <TouchableOpacity 
            style={styles.backButton}
            onPress={handleBack}
            disabled={!isReady || isLoading}
          >
            <Ionicons name="arrow-back" size={24} color="white" />
          </TouchableOpacity>
          <TouchableOpacity 
            style={[styles.flipButton, styles.iconGap]}
            onPress={pickFromGallery}
            disabled={isLoading}
          >
            <Ionicons name="image-outline" size={24} color="white" />
          </TouchableOpacity>
        </View>
        
        <TouchableOpacity 
          style={[
            styles.captureButton,
            (!cameraReady || isLoading) && styles.captureButtonDisabled
          ]} 
          onPress={takePicture}
          disabled={!cameraReady || isLoading}
        >
          {isLoading ? (
            <ActivityIndicator color="white" />
          ) : (
            <View style={styles.captureButtonInner} />
          )}
        </TouchableOpacity>

        <View style={styles.controlsGroup}>
          <TouchableOpacity 
            style={[
              styles.flipButton,
              !cameraReady && styles.buttonDisabled
            ]}
            onPress={toggleCameraType}
            disabled={!cameraReady || isLoading}
          >
            <Ionicons name="camera-reverse" size={28} color="white" />
          </TouchableOpacity>
        </View>
      </View>
      
      {!cameraReady && (
        <View style={styles.cameraLoadingOverlay}>
          <ActivityIndicator size="large" color="white" />
          <Text style={styles.cameraLoadingText}>Preparing camera...</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#000',
  },
  loadingText: {
    color: 'white',
    marginTop: 16,
    fontSize: 16,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#000',
    padding: 20,
  },
  errorIcon: {
    marginBottom: 20,
  },
  errorText: {
    color: 'white',
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 20,
    paddingHorizontal: 20,
  },
  retryButton: {
    backgroundColor: '#ff3b30',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    marginVertical: 8,
    minWidth: 200,
    alignItems: 'center',
  },
  retryText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  camera: {
    flex: 1,
    width: '100%',
  },
  overlay: {
    flex: 1,
    backgroundColor: 'transparent',
    justifyContent: 'space-between',
  },
  overlayTop: {
    height: '30%',
    width: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  overlayBottom: {
    height: '30%',
    width: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    
  },
  frameContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginHorizontal: 40,
  },
  frameCorner: {
    position: 'absolute',
    width: 40,
    height: 40,
    borderColor: 'white',
  },
  frameCornerTopLeft: {
    top: 0,
    left: 0,
    borderLeftWidth: 3,
    borderTopWidth: 3,
    borderTopLeftRadius: 10,
  },
  frameCornerTopRight: {
    top: 0,
    right: 0,
    borderRightWidth: 3,
    borderTopWidth: 3,
    borderTopRightRadius: 10,
  },
  frameCornerBottomLeft: {
    bottom: 0,
    left: 0,
    borderLeftWidth: 3,
    borderBottomWidth: 3,
    borderBottomLeftRadius: 10,
  },
  frameCornerBottomRight: {
    bottom: 0,
    right: 0,
    borderRightWidth: 3,
    borderBottomWidth: 3,
    borderBottomRightRadius: 10,
    
  },
  controls: {
    position: 'absolute',
    bottom: 60,
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 30,
  },
  controlsGroup: {
    flexDirection: 'row',
    alignItems: 'center',
    right: -5,
  },
  backButton: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    right: 20,
  },
  captureButton: {
    width: 70,
    height: 70,
    borderRadius: 35,
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 3,
    borderColor: 'white',
    right: 32,
  },
  captureButtonDisabled: {
    opacity: 0.5,
  },
  captureButtonInner: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: 'white',
    
  },
  flipButton: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    right: 20,
  },
  iconGap: { marginLeft: 10 },
  buttonDisabled: {
    opacity: 0.5,
  },
  cameraLoadingOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  cameraLoadingText: {
    color: 'white',
    marginTop: 16,
    fontSize: 16,
  },
});