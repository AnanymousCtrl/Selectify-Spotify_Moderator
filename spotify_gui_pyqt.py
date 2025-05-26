import sys
import threading
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
    QGridLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
import spotipy
from spotify_token_manager import SpotifyTokenManager

class SpotifyLanguagePlayerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spotify: My-Choice")

        
        client_id = '7240f6b32424485991cda36824b43683'
        client_secret = 'cd6fb4f3e2e44d82b99114f41762ef90'
        refresh_token = 'AQDLlMP8c9t9Jha-5MJEb561UaXx1lBajP4nxsnbiyFbskj1osvodiHmVKgx4DzXN466pnoAWkXTwFszROhgrnolMFJTbZnv6iwpAbU5qaS52y80v3Fb5Ez_xnFsM1VjRgU'

        self.token_manager = SpotifyTokenManager(client_id, client_secret, refresh_token)

        access_token = self.token_manager.get_access_token()
        self.sp = spotipy.Spotify(auth=access_token)

        self.next_batch_clicked = False

        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        layout = QGridLayout()

        layout.addWidget(QLabel("First Language:"), 0, 0)
        self.language1_entry = QLineEdit()
        layout.addWidget(self.language1_entry, 0, 1, 1, 2)

        layout.addWidget(QLabel("Second Language:"), 1, 0)
        self.language2_entry = QLineEdit()
        layout.addWidget(self.language2_entry, 1, 1, 1, 2)

        layout.addWidget(QLabel("Number of Songs:"), 2, 0)
        self.num_songs_entry = QLineEdit()
        layout.addWidget(self.num_songs_entry, 2, 1, 1, 2)

        self.start_button = QPushButton("Start Playing")
        self.start_button.clicked.connect(self.start_playback_thread)
        layout.addWidget(self.start_button, 3, 0)

        self.next_button = QPushButton("Next Batch")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.next_batch)
        layout.addWidget(self.next_button, 3, 1)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button, 3, 2)

        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text, 4, 0, 1, 3)

        self.setLayout(layout)
        self.resize(600, 400)

    def apply_styles(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#004080"))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor("#e0f7fa"))
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, QColor("#1DB954"))
        palette.setColor(QPalette.ButtonText, Qt.white)
        self.setPalette(palette)

        font = QFont("Segoe UI", 10)
        self.setFont(font)

        self.start_button.setStyleSheet("background-color: #1DB954; color: white; font-weight: bold;")
        self.next_button.setStyleSheet("background-color: #1DB954; color: white; font-weight: bold;")
        self.exit_button.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        self.status_text.setStyleSheet("background-color: #e0f7fa; color: black;")

        self.language1_entry.setStyleSheet("color: black; background-color: #e0f7fa;")
        self.language2_entry.setStyleSheet("color: black; background-color: #e0f7fa;")
        self.num_songs_entry.setStyleSheet("color: black; background-color: #e0f7fa;")

    def log_status(self, message):
        self.status_text.append(message)

    def refresh_spotify_token(self):
        access_token = self.token_manager.get_access_token()
        self.sp = spotipy.Spotify(auth=access_token)

    def search_tracks_by_language(self, language, limit=50):
        self.refresh_spotify_token()
        results = self.sp.search(q=language, type='track', limit=limit)
        tracks = results['tracks']['items']
        track_uris = [track['uri'] for track in tracks]
        return track_uris

    def play_tracks(self, track_uris):
        self.refresh_spotify_token()
        if not track_uris:
            self.log_status("No tracks to play.")
            return
        self.sp.start_playback(uris=track_uris)

    def next_batch(self):
        self.next_batch_clicked = True

    def playback_loop(self, language1, language2, x):
        tracks_lang1 = self.search_tracks_by_language(language1, limit=50)
        tracks_lang2 = self.search_tracks_by_language(language2, limit=50)

        import random
        random.shuffle(tracks_lang1)
        random.shuffle(tracks_lang2)

        index1, index2 = 0, 0
        total1, total2 = len(tracks_lang1), len(tracks_lang2)

        while index1 < total1 or index2 < total2:
            if index1 < total1:
                end1 = min(index1 + x, total1)
                self.log_status(f"Playing {language1} songs {index1 + 1} to {end1}")
                self.play_tracks(tracks_lang1[index1:end1])
                self.next_button.setEnabled(True)
                self.next_batch_clicked = False
                while not self.next_batch_clicked:
                    QApplication.processEvents()
                self.next_button.setEnabled(False)
                index1 = end1

            if index2 < total2:
                end2 = min(index2 + x, total2)
                self.log_status(f"Playing {language2} songs {index2 + 1} to {end2}")
                self.play_tracks(tracks_lang2[index2:end2])
                self.next_button.setEnabled(True)
                self.next_batch_clicked = False
                while not self.next_batch_clicked:
                    QApplication.processEvents()
                self.next_button.setEnabled(False)
                index2 = end2

    def start_playback_thread(self):
        language1 = self.language1_entry.text().strip().lower()
        language2 = self.language2_entry.text().strip().lower()
        try:
            x = int(self.num_songs_entry.text())
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter a valid number for songs.")
            return

        if not language1 or not language2:
            QMessageBox.critical(self, "Input Error", "Please enter both languages.")
            return

        self.log_status(f"Starting playback: {x} songs alternating between {language1} and {language2}...")

        self.next_button.setEnabled(False)
        threading.Thread(target=self.playback_loop, args=(language1, language2, x), daemon=True).start()

if __name__ == "__main__":
    app = QApplication([])
    window = SpotifyLanguagePlayerApp()
    window.show()
    sys.exit(app.exec_())