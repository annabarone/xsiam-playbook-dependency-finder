import os
from dotenv import load_dotenv


load_dotenv()


def get_demisto_path() -> str:
    DEMISTO_CONTENT_PACK_DIR_PATH = os.environ.get('DEMISTO_CONTENT_PACK_DIR_PATH')
    if os.path.basename(DEMISTO_CONTENT_PACK_DIR_PATH) == "Packs":
        return DEMISTO_CONTENT_PACK_DIR_PATH
    else:
        return os.path.join(DEMISTO_CONTENT_PACK_DIR_PATH, "Packs")