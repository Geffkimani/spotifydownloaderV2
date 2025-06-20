import logging

logging.basicConfig(
    filename="spotify_downloader.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
