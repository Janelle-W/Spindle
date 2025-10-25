from llama_cpp.server.app import create_app
from llama_cpp.server.settings import ServerSettings, ModelSettings
import threading
import os
import sys
import uvicorn

def resource_path(relative_path):
    """Resolve paths correctly for PyInstaller bundles"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def start_llama_server():
    # --- Configuration (placeholders, no hardcoded values) ---
    model_file = resource_path(
        os.getenv("SPINDLE_LLAMA_MODEL", "YOUR_MODEL_FILE_PATH_HERE")  
        # e.g., "./models/llama-2-13b-chat.Q4_K_M.gguf"
    )

    server_settings = ServerSettings(
        host=os.getenv("SPINDLE_LLAMA_HOST", "YOUR_HOST_HERE"),   # e.g., "0.0.0.0"
        port=int(os.getenv("SPINDLE_LLAMA_PORT", "YOUR_PORT_HERE"))  # e.g., "8000"
    )

    model_settings = [
        ModelSettings(
            model=model_file,
            n_ctx=int(os.getenv("SPINDLE_LLAMA_CTX", "2048"))  # context size placeholder
        )
    ]

    app = create_app(
        server_settings=server_settings,
        model_settings=model_settings
    )

    # Launch FastAPI app in background
    threading.Thread(
        target=lambda: uvicorn.run(
            app,
            host=server_settings.host,
            port=server_settings.port
        ),
        daemon=True
    ).start()
