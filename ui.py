import gradio as gr
from spotify_api import get_tracks_from_playlist
from utils import download_all_tracks


def handle_fetch(url):
    try:
        tracks = get_tracks_from_playlist(url)
        if not tracks:
            raise ValueError("No tracks found in the playlist.")

        # Format display labels and preserve IDs
        display_names = [f"{t['name']} - {t['artists'][0]['name']}" for t in tracks]
        track_map = {t["id"]: t for t in tracks}

        return (
            gr.update(choices=display_names, value=display_names, visible=True),
            gr.update(visible=True),
            track_map,
            f"✅ Loaded {len(tracks)} track(s) from playlist."
        )
    except Exception as e:
        return (
            gr.update(choices=[], value=[], visible=False),
            gr.update(visible=False),
            {},
            f"❌ Error: {str(e)}"
        )


def handle_download(selected_display_names, track_map):
    if not selected_display_names:
        return "⚠️ No tracks selected."

    # Map display names back to track objects
    selected_tracks = []
    for t in track_map.values():
        label = f"{t['name']} - {t['artists'][0]['name']}"
        if label in selected_display_names:
            selected_tracks.append(t)

    download_all_tracks(selected_tracks)
    return f"✅ Downloaded {len(selected_tracks)} track(s)!"


def launch_ui():
    with gr.Blocks(title="Spotify Playlist Downloader") as demo:
        gr.Markdown("## 🎧 Spotify Playlist Downloader")
        gr.Markdown("Paste a Spotify playlist URL and select which tracks to download as MP3.")

        url_input = gr.Textbox(label="Spotify Playlist URL", placeholder="Paste URL here...")
        fetch_btn = gr.Button("🔍 Fetch Tracks")
        download_btn = gr.Button("⬇️ Download Selected Tracks", visible=False)
        track_selector = gr.CheckboxGroup(label="Tracks in Playlist", visible=False)
        status_box = gr.Textbox(label="Status", interactive=False)
        track_state = gr.State({})  # {track_id: track_data}

        fetch_btn.click(
            fn=handle_fetch,
            inputs=url_input,
            outputs=[track_selector, download_btn, track_state, status_box]
        )

        download_btn.click(
            fn=handle_download,
            inputs=[track_selector, track_state],
            outputs=status_box
        )

    demo.launch()


if __name__ == "__main__":
    launch_ui()
