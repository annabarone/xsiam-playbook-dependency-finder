import json
import os

import yaml
from dotenv import load_dotenv

from utils import get_demisto_path

load_dotenv()

by_pack_list = {}
by_script_list = {}
sub_dir_mapping = "mappings/content_type_to_packs.json"
content_pack_dir = get_demisto_path()

print("INFO: Starting mapping scripts to packs.")

try:
    # Grab directories that only have Scripts
    with open(sub_dir_mapping, "r") as f:
        mapping = json.load(f)

    all_content_packs = [os.path.join(content_pack_dir, x) for x in mapping.get("Scripts", [])]
    for content_pack in all_content_packs:
        pack_name = os.path.basename(content_pack)
        if "Scripts" in os.listdir(content_pack):
            by_pack_list[pack_name] = []
            scripts_dir = os.path.join(content_pack, "Scripts")
            for script in os.listdir(scripts_dir):
                script_dir = os.path.join(scripts_dir, script)
                if not os.path.isdir(script_dir):
                    if ".yml" in script_dir:
                        yml = script_dir
                    else:
                        print(f"WARNING: Script not dir structure nor yml: {script_dir}")
                        continue
                else:
                    yml_files = [x for x in os.listdir(script_dir) if ".yml" in x]
                    if len(yml_files) != 1:
                        print(f"YML files not == 1: {script_dir}")
                        continue
                    yml = os.path.join(script_dir, yml_files[0])

                with open(yml, "r") as f:
                    data = yaml.safe_load(f)

                script_name = data.get("id") if data.get("id") else data.get("name")
                # Mapping by pack
                by_pack_list[pack_name].append(script_name)

                # Mapping by the script name for easier finding
                if by_script_list.get(script_name):
                    by_script_list[script_name].append(pack_name)
                else:
                    by_script_list[script_name] = [pack_name]

except Exception as e:
    pass


with open("mappings/pack_to_scripts.json", "w") as f:
    json.dump(by_pack_list, f, indent=4)

with open("mappings/script_to_packs.json", "w") as f:
    json.dump(by_script_list, f, indent=4)

print("INFO: Finished mapping scripts to packs.")
