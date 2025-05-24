# Spotify: My-Choice

This is a Python application that connects to your Spotify account and plays songs alternating between two specified languages. The app allows you to specify the number of songs to play from each language before switching to the other.

## Features

- Connects to Spotify using OAuth with automatic token refreshing.
- User-friendly PyQt5 GUI for inputting languages and number of songs.
- Playback control with "Start Playing", "Next Batch", and "Exit" buttons.
- Randomized song order to avoid repetitive playback.
- Handles long playback sessions with automatic access token refresh.

## Requirements

- Python 3.7+
- spotipy
- PyQt5
- requests (for token refreshing)

## Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:

   ```bash
   pip install spotipy PyQt5 requests
   ```

3. Register your app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) to obtain:

   - Client ID
   - Client Secret
   - Set a Redirect URI (needed for OAuth flow)

4. Obtain a refresh token by performing the Spotify OAuth authorization code flow. You can use the Spotipy library or a custom script to do this.

5. Update the `spotify_token_manager.py` file with your `client_id`, `client_secret`, and `refresh_token`.

6. Update the `spotify_gui_pyqt.py` file with your Spotify app credentials in the designated section.

## Running the Application

Run the PyQt5 GUI application:

```bash
python spotify_gui_pyqt.py
```

Enter the two languages and the number of songs to play from each language, then click "Start Playing". Use the "Next Batch" button to proceed through batches of songs.

## Notes

- The access token is refreshed automatically during runtime using the refresh token.
- The song order is randomized each time playback starts to provide variety.
- Ensure your Spotify app has the necessary scopes for playback control.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [Spotipy](https://spotipy.readthedocs.io/en/2.19.0/) - Python client for the Spotify Web API
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - Python bindings for the Qt application framework
