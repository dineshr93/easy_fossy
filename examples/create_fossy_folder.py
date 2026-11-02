"""Create (or reuse) the Fossology folder layout for a project.

    <parent: PROJECT_NAME> / <PROJECT_NAME-dd-mm-yyyy>

Usage:
    python3 create_fossy_folder.py config.ini fossy_server PROJECT_NAME [--root-folder-id 1]

The id of the dated sub folder is printed as the LAST line of stdout, so a
Jenkins shell step can capture it:

#create a folder under project name folder with date appended 
folder_id=$(python3 create_fossy_folder.py "$config_file" "$fossy_server" "$PROJECT_NAME" | tail -1)
if ! [[ "$folder_id" =~ ^[0-9]+$ ]]; then
    echo "Failed to create/find fossy folder: '$folder_id'"
    exit 1
fi
"""

import argparse
import datetime
import sys

from easy_fossy import easy_fossy as fossy


def find_folder(folders, name, parent_id):
    return next(
        (f for f in folders if f.name == name and f.parent == parent_id), None
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("config_file")
    ap.add_argument("server")
    ap.add_argument("project_name")
    ap.add_argument(
        "--root-folder-id",
        type=int,
        default=1,
        help="folder under which the project parent folder lives (default: 1)",
    )
    args = ap.parse_args()

    use_fossy_to = fossy(args.config_file, args.server)
    folders = use_fossy_to.get_all_folders() or []

    parent = find_folder(folders, args.project_name, args.root_folder_id)
    if parent:
        parent_id = parent.id
    else:
        info = use_fossy_to.create_folder_under_parent_folder_id(
            args.root_folder_id, args.project_name
        )
        parent_id = int(info.message)

    sub_name = f"{args.project_name}-{datetime.date.today():%d-%m-%Y}"
    sub = find_folder(folders, sub_name, parent_id)
    if sub:
        folder_id = sub.id
    else:
        info = use_fossy_to.create_folder_under_parent_folder_id(parent_id, sub_name)
        folder_id = int(info.message)

    print(folder_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
