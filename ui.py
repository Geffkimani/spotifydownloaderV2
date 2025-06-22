import gradio as gr
import json
import os
import logging
from spotify_api import get_tracks_from_playlist
from utils import download_track_with_status

# Setup
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)
logging.basicConfig(filename=os.path.join(LOGS_DIR, "web_ui.log"), level=logging.INFO)

def fetch_tracks(url):
    """
    Fetch tracks from Spotify playlist URL.
    """
    try:
        tracks = get_tracks_from_playlist(url)
        choices = [f"{t['name']} - {t['artists'][0]['name']}" for t in tracks]
        # Store the full track info for later download
        return choices, tracks, "✅ Tracks loaded."
    except Exception as e:
        logging.error(f"Error loading playlist: {e}")
        return [], [], f"❌ Error: {str(e)}"

def download_selected(selected_titles, full_tracks):
    """
    Download selected tracks by matching titles.
    """
    if not selected_titles:
        return "⚠️ No tracks selected."

    results = []
    for track in full_tracks:
        title = f"{track['name']} - {track['artists'][0]['name']}"
        if title in selected_titles:
            success = download_track_with_status(title)
            status = "✅ Success" if success else "❌ Failed"
            results.append(f"{title} — {status}")
    return "\n".join(results)

def launch_ui():
    with gr.Blocks(title="🎧 Spotify Downloader") as demo:
        gr.Markdown("## 🎵 Spotify Playlist Downloader")
        gr.Markdown("Paste a Spotify playlist URL. View and select songs to download.")

        url_input = gr.Textbox(label="Spotify Playlist URL")
        fetch_button = gr.Button("🔍 Fetch Songs")

        song_selector = gr.CheckboxGroup(label="Select Songs", choices=[], visible=False)
        full_track_state = gr.State([])

        download_button = gr.Button("⬇️ Download Selected", visible=False)
        output_box = gr.Textbox(label="Status", lines=10, interactive=False)

        def handle_fetch(url):
            titles, full_tracks, status = fetch_tracks(url)
            return (
                gr.update(choices=titles, visible=True, value=[]),
                full_tracks,
                gr.update(value=status),
                gr.update(visible=True)
            )

        def handle_download(selected_titles, full_tracks):
            return download_selected(selected_titles, full_tracks)

        fetch_button.click(
            fn=handle_fetch,
            inputs=url_input,
            outputs=[song_selector, full_track_state, output_box, download_button]
        )

        download_button.click(
            fn=handle_download,
            inputs=[song_selector, full_track_state],
            outputs=output_box
        )

    demo.launch()
