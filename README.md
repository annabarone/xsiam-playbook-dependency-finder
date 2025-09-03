# Cortex XSIAM - Playbook Dependency Finder

This tool helps you find the dependencies of your Cortex XSIAM playbooks. It identifies the commands, scripts, and 
sub-playbooks that your playbooks use, and determines the specific integrations or marketplace packs required.

## Prerequisites

Before you begin, ensure you have the following:

*   Python 3 installed on your system.
*   The `demisto/content` repository cloned locally. You can clone it from here: [https://github.com/demisto/content](https://github.com/demisto/content)

## Setup

1.  **Create a `.env` file:**

    Create a file named `.env` in the root of this project. It should contain the following variables:

    ```
    REPO_PATH=/path/to/your/playbook/repository/
    DEMISTO_CONTENT_PACK_DIR_PATH=/path/to/your/cloned/content/repository
    ```

    *   `REPO_PATH`: The absolute path to the repository containing the XSIAM playbooks you want to analyze.
    *   `DEMISTO_CONTENT_PACK_DIR_PATH`: The absolute path to the directory where you cloned the `demisto/content` repository

2.  **Run the setup script:**

    Execute the `setup.sh` script to set up the environment and generate the necessary mappings.

    ```bash
    bash setup.sh
    ```

## Usage

To find the dependencies, run the `dependency_finder.py` script using the `run.sh` script.

```bash
bash run.sh
```

## Output

The script will generate a CSV file named `playbook_dependencies.csv`. This file will contain the following columns:

*   **Playbook Filename:** The name of the playbook in your repo.
*   **Task Command:** The name of the task within the playbook.
*   **Script:** The script of the task within the playbook
*   **Sub-Playbook:** The sub-playbook of the task within the playbook
*   **Source Integration:** If specified, the source integration for the command
*   **MarketPlace Pack:** The Marketplace Pack analyzed for the command


## Helpers
You can import the .CSV files into Google Sheets, and use conditional formatting to understand requirements a bit more. 
These conditional rules help: 

#### Highlight Potentially Custom Content 

* **Description**: Highlights any script/playbook row that has content not found in the demisto/content repo
* **Apply to Range**: C1:D1000
* **Format Rules**: _Custom formula is_
* **Custom Formula**: _=$F1="? Not in MP - Custom?"_


#### Highlight Unique MP Packs 

* **Description**: Highlights the first instance of any MP pack specified to visually dedup
* **Apply to Range**: F1:F1000
* **Format Rules**: _Custom formula is_
* **Custom Formula**: _=MATCH(F1,F:F,0)=ROW()_

