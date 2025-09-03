import os
import json
import yaml
import datetime
from dotenv import load_dotenv

from utils import get_demisto_path

load_dotenv()

by_pack_mapping = {}
by_command_mapping = {}
integration_to_pack_mapping = {}
sub_dir_mapping = "mappings/content_type_to_packs.json"
content_pack_dir = get_demisto_path()


print("INFO: Starting mapping Integration Commands to packs.")

try:
    # Grab directories that only have Integrations
    with open(sub_dir_mapping, "r") as f:
        mapping = json.load(f)

    all_content_packs = [os.path.join(content_pack_dir, x) for x in mapping.get("Integrations", [])]
    for content_pack in all_content_packs:
        pack_name = os.path.basename(content_pack)
        if "Integrations" in os.listdir(content_pack):
            integrations_dir = os.path.join(content_pack, "Integrations")
            for integration in os.listdir(integrations_dir):
                integration_dir = os.path.join(integrations_dir, integration)
                if not os.path.isdir(integration_dir):
                    if ".yml" in integration_dir:
                        yml = integration_dir
                    else:
                        print(f"WARNING: Integration not dir structure nor yml: {integration_dir}")
                        continue
                else:
                    yml_files = [x for x in os.listdir(integration_dir) if ".yml" in x]
                    if len(yml_files) != 1:
                        print(f"YML files not == 1: {integration_dir}")
                        continue
                    yml = os.path.join(integration_dir, yml_files[0])

                with open(yml, "r") as f:
                    data = yaml.safe_load(f)

                integration_name = data.get("name")
                commands = [x.get("name") for x in data.get("script", {}).get("commands", [])]
                by_pack_mapping[integration_dir] = commands

                for cmd in commands:
                    if by_command_mapping.get(cmd):
                        by_command_mapping[cmd].append(integration_dir)
                    else:
                        by_command_mapping[cmd] = [integration_dir]

                if integration_to_pack_mapping.get(integration_name):
                    integration_to_pack_mapping[integration_name].append(pack_name)
                else:
                    integration_to_pack_mapping[integration_name] = [pack_name]

except Exception as e:
    pass

with open("mappings/pack_to_integration_commands.json", "w") as f:
    json.dump(by_pack_mapping, f, indent=4)

with open("mappings/integration_commands_to_packs.json", "w") as f:
    json.dump(by_command_mapping, f, indent=4)

with open("mappings/integration_to_packs.json", "w") as f:
    json.dump(integration_to_pack_mapping, f, indent=4)

print("INFO: Finished mapping Integration Commands to packs.")
