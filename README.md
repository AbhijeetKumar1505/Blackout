# Blackout Screen Prank (Mobile)

A fun mobile prank application that creates a fake system blackout screen with sound effects and screen freezing capability.

## Features

- Fullscreen black overlay
- Flickering "System Blackout" message
- Interactive "Fix" button with sound effect
- Screen freeze functionality
- Auto-close after 10 seconds
- Works on Android devices

## Development Setup

1. Install Python 3.8 or higher
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. For Android development, install additional requirements:
   - Java JDK 8
   - Android SDK
   - Android NDK
   - Buildozer

## Running on Desktop (Development)

For testing during development:
```
python main.py
```

## Building for Android

1. Install buildozer:
   ```
   pip install buildozer
   ```

2. Initialize buildozer (already done):
   ```
   buildozer init
   ```

3. Build the Android APK:
   ```
   buildozer android debug
   ```

4. The APK will be generated in the `bin` directory

## Installing on Android

1. Enable "Install from Unknown Sources" in your Android settings
2. Transfer the generated APK to your Android device
3. Install the APK by tapping on it
4. Grant the requested permissions when prompted

## Usage

1. Launch the app
2. The screen will go black with a flickering message
3. Use the "Freeze Screen" button to freeze/unfreeze the display
4. Click the "Fix" button to play the sound effect
5. The app will close automatically after 10 seconds
6. Use the back button to exit at any time

## Permissions Required

- Storage access (for sound files)
- System alert window (for screen freeze functionality)

## Note

This is a harmless prank application. The screen will return to normal after closing the application or pressing the back button. 