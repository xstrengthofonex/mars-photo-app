import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_DIR = os.path.join(ROOT_DIR, "static")

PORT = int(os.environ.get("PORT", 8000))
