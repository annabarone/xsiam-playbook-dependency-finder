import json
import os

from dotenv import load_dotenv

from utils import get_demisto_path

load_dotenv()

mapping = {}
content_pack_dir = get_demisto_path()

print("INFO: Starting mapping marketplace packs to their available content types.")

try:
    all_content_packs = [os.path.join(content_pack_dir, x) for x in os.listdir(content_pack_dir) if os.path.isdir(os.path.join(content_pack_dir, x))]
    for content_pack in all_content_packs:
        pack_name = os.path.basename(content_pack)
        sub_dirs = [os.path.join(content_pack, x) for x in os.listdir(content_pack) if os.path.isdir(os.path.join(content_pack, x))]
        for sub_dir in sub_dirs:
            sub_dir_name = os.path.basename(sub_dir)
            if not mapping.get(sub_dir_name):
                mapping[sub_dir_name] = [pack_name]
            else:
                mapping[sub_dir_name].append(pack_name)

except Exception as e:
    pass

with open("mappings/content_type_to_packs.json", "w") as f:
    json.dump(mapping, f, indent=4)

print('Finished mapping marketplace packs to their available content types.')
