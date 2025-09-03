import json
import os

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel

from utils import get_demisto_path


class Entry(BaseModel):
    playbook_name: str
    task_name: str
    script: str = ""
    command: str = ""
    playbook: str = ""
    source: str = ""
    mp_pack: str = ""


load_dotenv()
demisto_content_path = get_demisto_path()
repo_path = os.environ.get('REPO_PATH')
repo_name = repo_path.split('/')[-1]
if not os.path.exists(repo_path):
    print("ERROR: Repo in .env file doesn't exist.")
    exit(-1)

integration_commands_file = "mappings/integration_commands_to_packs.json"
integrations_file = "mappings/integration_to_packs.json"
scripts_file = "mappings/script_to_packs.json"
playbooks_file = "mappings/playbook_to_packs.json"
with open(integration_commands_file, "r") as f:
    integration_commands_mappings = json.load(f)
with open(scripts_file, "r") as f:
    scripts_mappings = json.load(f)
with open(integrations_file, "r") as f:
    integration_mappings = json.load(f)
with open(playbooks_file, "r") as f:
    playbooks_mappings = json.load(f)


if not os.path.exists(f"{repo_path}/Playbooks"):
    print("ERROR: Repo has no Playbooks")
    exit()

playbooks = [os.path.join(f"{repo_path}/Playbooks", x) for x in os.listdir(f"{repo_path}/Playbooks")]
dependencies = {x: [] for x in playbooks}

print(f"INFO: Starting finding dependencies for repo in {repo_path}")
# Consolidate the tasks from the playbook file
for playbook_file in playbooks:
    if not playbook_file:
        print(f"NO PLAYBOOK FILE FOUND: {playbook_file}")
        continue

    with open(playbook_file, "r") as f:
        data = yaml.safe_load(f)
        for task in data["tasks"].values():
            if task.get("type") in ["playbook", "regular"]:
                dependencies[playbook_file].append(task.get("task"))


entries = []
for playbook, tasks in dependencies.items():
    for task in tasks:
        if task.get("type") in ["playbook", "regular"]:
            entry = Entry(
                playbook_name=playbook.replace(".yml", "").replace(f"{repo_path}/Playbooks/", ""),
                task_name=task.get("name"))
            if task.get("type") in ["playbook"]:
                entry.playbook = task.get("playbookName") if task.get("playbookName") else task.get("playbookId")
            else:
                if task.get("iscommand"):
                    entry.command = task.get("script")
                else:
                    entry.script = task.get("script") if task.get("script") else task.get('scriptName')
            if task.get("brand"):
                entry.source = task.get("brand")

                if entry.source.lower() == "builtin":
                    entry.mp_pack = "BuiltIn"

                # If brand specified, the source is an integration
                else:
                    integration_mp_pack = integration_mappings.get(entry.source, [])

                    if len(integration_mp_pack) == 1:
                        entry.mp_pack = integration_mp_pack[0]
                    elif len(integration_mp_pack) == 0:
                        entry.mp_pack = "? Integration not in content"
                    else:
                        entry.mp_pack = f"? {len(integration_mp_pack)} options"

            entries.append(entry)

# enrich the locations
for entry in entries:
    if entry.script:
        entry.mp_pack = scripts_mappings.get(entry.script, ['? Not in MP - Custom?'])[0]
    if entry.command:
        # commands are normally "|||core-run-script-execute-commands"
        split = entry.command.split("|||")
        defined_integration = split[0]
        defined_command = split[1]
        command_map = integration_commands_mappings.get(defined_command, [])

        # If the command is unique
        if len(command_map) == 1:
            location = command_map[0]
            integ = os.path.basename(location)
            pack = location.split("/")[-3]
            entry.source = integ if not entry.source else entry.source
            entry.mp_pack = pack

        else:
            if not entry.mp_pack:
                entry.mp_pack = f"? {len(command_map)} options"

    if entry.playbook:
        playbook_mp_pack = playbooks_mappings.get(entry.playbook, [])

        if len(playbook_mp_pack) == 1:
            entry.mp_pack = playbook_mp_pack[0]
        elif len(playbook_mp_pack) == 0:
            entry.mp_pack = "? Not in MP - Custom?"
        else:
            entry.mp_pack = f"? {len(playbook_mp_pack)} options"


output = []
output.append("Playbook Filename,Task Command,Script,Sub-Playbook,Source Integration,MarketPlace Pack")
for e in entries:
    output.append(f"{e.playbook_name},{e.command},{e.script},{e.playbook},{e.source},{e.mp_pack}")

with open(f"dependencies/dependencies-{repo_name}.csv", "w") as f:
    f.write('\n'.join(output))

print("\n\n-----\n\n")


# Determine if more playbooks to go down
# for p in task_keys['playbookName']:
#     if p not in first_round_playbooks and p not in second_round_playbooks and p not in third_round_playbooks:
#         print(f"'{p}',")

print(f"INFO: Finished finding dependencies for repo in {repo_path}")
