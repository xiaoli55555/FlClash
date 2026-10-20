import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

void main() {
  test('light and dark Android splash screens use the tdnv artwork', () {
    for (final qualifier in ['values-v27', 'values-night-v27']) {
      final source = File(
        'android/app/src/main/res/$qualifier/styles.xml',
      ).readAsStringSync();
      final icon = RegExp(
        r'<item\b[^>]*name="android:windowSplashScreenAnimatedIcon"[^>]*>([^<]+)</item>',
      ).firstMatch(source);
      expect(icon?.group(1), '@drawable/tdnv_launcher', reason: qualifier);
      final background = RegExp(
        r'<item\b[^>]*name="android:windowSplashScreenBackground"[^>]*>([^<]+)</item>',
      ).firstMatch(source);
      expect(
        background?.group(1),
        '@color/ic_launcher_background',
        reason: qualifier,
      );
    }
  });
}
