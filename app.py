import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import os

class BlackoutPrank(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Update")
        # Set window to fullscreen
        self.showFullScreen()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Set black background
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("black"))
        self.setPalette(palette)
        
        # Create message label with flicker effect
        self.message = QLabel("Oops! System Blackout!")
        self.message.setStyleSheet("""
            color: white;
            font-size: 48px;
            font-family: Arial;
        """)
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create fix button
        self.fix_button = QPushButton("Click to Fix")
        self.fix_button.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                font-size: 24px;
                background-color: #ff3030;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff0000;
            }
        """)
        self.fix_button.clicked.connect(self.on_fix_clicked)
        
        # Add widgets to layout
        layout.addWidget(self.message)
        layout.addWidget(self.fix_button)
        
        # Setup media player for sound
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        
        # Get the absolute path to the sound file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sound_path = os.path.join(current_dir, "static", "your-sound-file.mp3")
        self.player.setSource(QUrl.fromLocalFile(sound_path))
        
        # Setup flicker timer
        self.flicker_timer = QTimer()
        self.flicker_timer.timeout.connect(self.flicker_effect)
        self.flicker_timer.start(500)  # Flicker every 500ms
        
        # Setup reload timer
        self.reload_timer = None

    def flicker_effect(self):
        current_opacity = self.message.windowOpacity()
        self.message.setWindowOpacity(0.5 if current_opacity == 1.0 else 1.0)

    def on_fix_clicked(self):
        # Play sound
        self.audio_output.setVolume(1.0)
        self.player.play()
        
        # Setup reload timer
        self.reload_timer = QTimer()
        self.reload_timer.timeout.connect(self.close)
        self.reload_timer.start(10000)  # Close after 10 seconds

    def keyPressEvent(self, event):
        # Allow escape key to exit
        if event.key() == Qt.Key.Key_Escape:
            if self.reload_timer:
                self.reload_timer.stop()
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BlackoutPrank()
    window.show()
    sys.exit(app.exec())
