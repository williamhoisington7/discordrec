"""Standalone offline desktop launcher for the invitation letter UI."""

from __future__ import annotations

import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path

# Ensure project root is importable when frozen or run as a script.
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    ROOT = Path(sys._MEIPASS)
else:
    ROOT = Path(__file__).resolve().parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_for_server(host: str, port: int, timeout: float = 10.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.25):
                return
        except OSError:
            time.sleep(0.05)
    raise RuntimeError(f"Local invitation server did not start on {host}:{port}")


def configure_webview_downloads(webview_module) -> None:
    """Enable attachment downloads so the PDF button works in the desktop shell.

    pywebview cancels Content-Disposition downloads unless ALLOW_DOWNLOADS is true
    (see edgechromium.on_download_starting and equivalents on other platforms).
    """
    webview_module.settings["ALLOW_DOWNLOADS"] = True


def main() -> None:
    # Import after sys.path configuration so frozen builds resolve bundled modules.
    from app import app

    app.config["TEMPLATES_AUTO_RELOAD"] = False

    host = "127.0.0.1"
    port = _free_port()
    url = f"http://{host}:{port}/"

    def run_server() -> None:
        # use_reloader must stay false inside a frozen desktop app.
        app.run(host=host, port=port, debug=False, use_reloader=False, threaded=True)

    server = threading.Thread(target=run_server, daemon=True)
    server.start()
    _wait_for_server(host, port)

    title = "Would Kill For Pie — Invitation Studio"
    try:
        import webview
    except ImportError:
        webview = None

    if webview is not None:
        try:
            configure_webview_downloads(webview)
            webview.create_window(
                title,
                url,
                width=1180,
                height=860,
                min_size=(900, 700),
                background_color="#140c0a",
            )
            webview.start()
            return
        except Exception as error:
            print(f"Desktop window unavailable ({error!r}); opening local browser instead.")

    webbrowser.open(url)
    print(title)
    print(f"Offline UI running at {url}")
    print("Close this window to exit.")
    try:
        while server.is_alive():
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
