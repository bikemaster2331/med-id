import { Platform } from 'react-native';

export const fonts = {
  regular: Platform.select({ ios: 'System', android: 'sans-serif' })!,
  medium: Platform.select({ ios: 'System', android: 'sans-serif-medium' })!,
  semibold: Platform.select({ ios: 'System', android: 'sans-serif-medium' })!,
  bold: Platform.select({ ios: 'System', android: 'sans-serif' })!,
  display: Platform.select({ ios: 'System', android: 'sans-serif' })!,
};
