import json
import os

import yaml
from dotenv import load_dotenv

from utils import get_demisto_path

load_dotenv()

by_pack_list = {}
by_playbook_list = {}
sub_dir_mapping = "mappings/content_type_to_packs.json"
content_pack_dir = get_demisto_path()

print("INFO: Starting mapping playbooks to packs.")

try:
    # Grab directories that only have Scripts
    with open(sub_dir_mapping, "r") as f:
        mapping = json.load(f)

    all_content_packs = [os.path.join(content_pack_dir, x) for x in mapping.get("Playbooks", [])]
    for content_pack in all_content_packs:
        pack_name = os.path.basename(content_pack)
        if "Playbooks" in os.listdir(content_pack):
            by_pack_list[pack_name] = []
            playbooks_dir = os.path.join(content_pack, "Playbooks")
            for playbook in os.listdir(playbooks_dir):
                playbook_dir = os.path.join(playbooks_dir, playbook)
                if not os.path.isdir(playbook_dir):
                    if ".yml" in playbook_dir:
                        yml = playbook_dir
                    else:
                        print(f"WARNING: Playbook not dir structure nor yml: {playbook_dir}")
                        continue
                else:
                    yml_files = [x for x in os.listdir(playbook_dir) if ".yml" in x]
                    if len(yml_files) != 1:
                        print(f"YML files not == 1: {playbook_dir}")
                        continue
                    yml = os.path.join(playbook_dir, yml_files[0])

                with open(yml, "r") as f:
                    data = yaml.safe_load(f)

                playbook_name = data.get("id") if data.get("id") else data.get("name")
                # Mapping by pack
                by_pack_list[pack_name].append(playbook_name)

                # Mapping by the playbook name for easier finding
                if by_playbook_list.get(playbook_name):
                    by_playbook_list[playbook_name].append(pack_name)
                else:
                    by_playbook_list[playbook_name] = [pack_name]

except Exception as e:
    pass


with open("mappings/pack_to_playbooks.json", "w") as f:
    json.dump(by_pack_list, f, indent=4)

with open("mappings/playbook_to_packs.json", "w") as f:
    json.dump(by_playbook_list, f, indent=4)

print("INFO: Finished mapping playbooks to packs.")
