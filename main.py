from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.utils import platform
from kivy.config import Config
import os

# Disable the default escape key exit
Config.set('kivy', 'exit_on_escape', '0')

class BlackoutPrank(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set black background
        Window.clearcolor = (0, 0, 0, 1)
        
        # Create message label with flicker effect
        self.message = Label(
            text="Oops! System Blackout!",
            font_size='48sp',
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.message)
        
        # Load and start sound loop
        sound_file = 'static/your-sound-file.mp3'
        if platform == 'android':
            from android.storage import primary_external_storage_path
            sound_file = os.path.join(primary_external_storage_path(), 'your-sound-file.mp3')
        self.sound = SoundLoader.load(sound_file)
        if self.sound:
            self.sound.loop = True  # Enable looping
            self.sound.play()  # Start playing immediately
        
        # Setup flicker effect
        Clock.schedule_interval(self.flicker_effect, 0.5)
        
        # Bind keyboard for custom exit (Ctrl+F4)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        
        # Set up screen freeze
        self._setup_device_freeze()
        
        # Disable the back button on Android
        if platform == 'android':
            try:
                from jnius import autoclass
                activity = autoclass('org.kivy.android.PythonActivity').mActivity
                activity.onBackPressed = lambda: None  # Disable back button
            except Exception as e:
                print(f"Error disabling back button: {e}")

    def _setup_device_freeze(self):
        # Prevent window from being closed by window manager
        Window.borderless = True
        Window.always_on_top = True  # Keep window on top
        
        # Capture all touch events to prevent interaction with anything else
        Window.bind(on_touch_down=self._block_touch)
        Window.bind(on_touch_move=self._block_touch)
        Window.bind(on_touch_up=self._block_touch)
        
        # Set up screen freeze for Android
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([
                    Permission.READ_EXTERNAL_STORAGE, 
                    Permission.WRITE_EXTERNAL_STORAGE,
                    Permission.SYSTEM_ALERT_WINDOW  # For overlay permissions
                ])
                
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                activity = PythonActivity.mActivity
                
                # Hide system UI and prevent system gestures
                View = autoclass('android.view.View')
                activity.getWindow().getDecorView().setSystemUiVisibility(
                    View.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
                    View.SYSTEM_UI_FLAG_FULLSCREEN |
                    View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION |
                    View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN |
                    View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY |
                    View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                )
                
                # Try to prevent recent apps button from working
                WindowManager = autoclass('android.view.WindowManager$LayoutParams')
                activity.getWindow().addFlags(WindowManager.FLAG_TURN_SCREEN_ON |
                                            WindowManager.FLAG_DISMISS_KEYGUARD |
                                            WindowManager.FLAG_SHOW_WHEN_LOCKED |
                                            WindowManager.FLAG_KEEP_SCREEN_ON)
            except Exception as e:
                print(f"Error setting fullscreen: {e}")

    def _block_touch(self, instance, touch):
        # Block all touch events
        return True

    def flicker_effect(self, dt):
        self.message.opacity = 0.5 if self.message.opacity == 1 else 1

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        # Only allow Ctrl+F4 to exit
        # Keycode is a tuple of (keycode_id, keycode_string)
        if 'ctrl' in modifiers and keycode[1] == 'f4':
            if self.sound:
                self.sound.stop()
            App.get_running_app().stop()
        # Block all other key combinations
        return True

class BlackoutPrankApp(App):
    def build(self):
        return BlackoutPrank()

    def on_start(self):
        # Set fullscreen
        Window.fullscreen = 'auto'
        
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE,
                    Permission.SYSTEM_ALERT_WINDOW
                ])
            except Exception as e:
                print(f"Error requesting permissions: {e}")
                
    def on_pause(self):
        # Prevent app from pausing
        return True
        
    def on_resume(self):
        # Ensure we're still in fullscreen when resuming
        Window.fullscreen = 'auto'
        return True

if __name__ == '__main__':
    BlackoutPrankApp().run() 