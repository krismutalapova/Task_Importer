#!/usr/bin/env python3
import os
import re
import json
import argparse
import requests
from typing import List, Dict, Tuple, Optional

__version__ = "1.0.0"

API_KEY = os.getenv("TRELLO_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")
API_BASE = "https://api.trello.com/1"

headers = {"Accept": "application/json"}
auth = {"key": API_KEY, "token": TOKEN}


class MarkdownParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.tasks = []
        self.sections = []
        self.project_title = None

    def parse(self) -> List[Dict]:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Markdown file '{self.file_path}' not found!")

        with open(self.file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tasks = []
        current_section = "General"
        current_subsection = ""

        for line_num, line in enumerate(content.split("\n"), 1):
            original_line = line
            line = line.strip()

            # Detect main project title
            if line.startswith("# ") and self.project_title is None:
                self.project_title = line[2:].strip()
                continue

            # Detect section headers
            header_match = re.match(r"^(#{1,6})\s*(.+)", line)
            if header_match:
                level = len(header_match.group(1))
                title = header_match.group(2).strip()

                # Remove numbering from section titles
                title = re.sub(r"^\d+\.?\s*", "", title)

                if level <= 3:  # Main sections
                    current_section = title
                    current_subsection = ""
                else:  # Subsections
                    current_subsection = title

                self.sections.append({"level": level, "title": title, "line": line_num})
                continue

            # Detect checklist items
            checkbox_match = re.match(r"^-\s*\[([ xX])\]\s*(.+)", line)
            if checkbox_match:
                is_completed = checkbox_match.group(1).lower() == "x"
                task_name = checkbox_match.group(2).strip()

                # Skip if task already exists (handle duplicates)
                if not self._is_duplicate(task_name, tasks):
                    task = {
                        "name": task_name,
                        "completed": is_completed,
                        "section": current_section,
                        "subsection": current_subsection,
                        "line": line_num,
                        "original_line": original_line.strip(),
                    }
                    tasks.append(task)

        self.tasks = tasks
        return tasks

    def _is_duplicate(self, task_name: str, existing_tasks: List[Dict]) -> bool:
        task_lower = task_name.lower()

        for existing in existing_tasks:
            existing_lower = existing["name"].lower()

            # Exact match
            if task_lower == existing_lower:
                return True

            # High similarity
            if len(task_lower) > 10 and len(existing_lower) > 10:
                common_words = set(task_lower.split()) & set(existing_lower.split())
                if len(common_words) >= 3:
                    return True

        return False


class TaskCategorizer:
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()

    def _default_config(self) -> Dict:
        return {
            "labels": [
                {"name": "Setup", "color": "green"},
                {"name": "Model", "color": "yellow"},
                {"name": "View", "color": "orange"},
                {"name": "Template/Frontend", "color": "purple"},
                {"name": "Form", "color": "blue"},
                {"name": "API/DRF", "color": "red"},
                {"name": "Messaging", "color": "sky"},
                {"name": "Rating", "color": "pink"},
                {"name": "Testing", "color": "lime"},
                {"name": "Optional", "color": "black"},
                {"name": "Security", "color": "black"},
            ],
            "lists": [
                {"name": "Backlog", "pos": "top"},
                {"name": "To Do", "pos": "bottom"},
                {"name": "In Progress", "pos": "bottom"},
                {"name": "Review", "pos": "bottom"},
                {"name": "Done", "pos": "bottom"},
            ],
            "categorization_rules": {
                "Setup": [
                    "setup",
                    "configure",
                    "install",
                    "create initial",
                    "project initialization",
                    "superuser",
                ],
                "Model": ["model", "database", "field", "extend user", "signals"],
                "View": ["view", "page", "redirect", "navigation", "handler"],
                "Template/Frontend": [
                    "template",
                    "ui",
                    "design",
                    "styling",
                    "frontend",
                    "responsive",
                    "glassmorphism",
                    "modern",
                    "card",
                    "footer",
                    "header",
                ],
                "Form": ["form", "validation", "signup", "login", "logout", "password"],
                "API/DRF": ["api", "signals", "auto-creation"],
                "Messaging": [
                    "message",
                    "messaging",
                    "contact",
                    "inbox",
                    "conversation",
                ],
                "Rating": ["rating", "review", "feedback"],
                "Testing": ["test", "testing", "documentation", "unit test"],
                "Security": ["security", "password", "auth", "session"],
                "Optional": ["optional", "enhancement", "additional", "advanced"],
            },
            "list_mapping": {
                "completed": "Done",
                "in_progress": "In Progress",
                "todo": "To Do",
                "backlog": "Backlog",
            },
        }

    def categorize(self, task: Dict) -> List[str]:
        task_text = (
            f"{task['name']} {task['section']} {task.get('subsection', '')}".lower()
        )

        labels = []

        for label_name, keywords in self.config["categorization_rules"].items():
            if any(keyword in task_text for keyword in keywords):
                labels.append(label_name)

        # Default label
        if not labels:
            labels.append("Setup")

        return labels

    def determine_list(self, task: Dict) -> str:
        if task["completed"]:
            return self.config["list_mapping"]["completed"]
        else:
            return self.config["list_mapping"]["todo"]


class TrelloAPI:
    def __init__(self):
        if not API_KEY or not TOKEN:
            print("❌ ERROR: Missing Trello API credentials!")
            print("")
            print("🔧 To fix this:")
            print("1. Go to https://trello.com/app-key")
            print("2. Copy your API Key")
            print("3. Generate a Token and copy it")
            print("4. Run these commands (replace with your actual values):")
            print("   export TRELLO_KEY=your_api_key_here")
            print("   export TRELLO_TOKEN=your_token_here")
            print("5. Run the script again in the same terminal")
            print("")
            raise ValueError(
                "Please set TRELLO_KEY and TRELLO_TOKEN environment variables"
            )

    def create_board(self, name: str) -> str:
        resp = requests.post(f"{API_BASE}/boards", params={**auth, "name": name})
        resp.raise_for_status()
        board_id = resp.json()["id"]

        # Remove default lists that Trello creates automatically
        self.remove_default_lists(board_id)

        return board_id

    def create_labels(self, board_id: str, labels: List[Dict]) -> Dict[str, str]:
        label_map = {}
        for lbl in labels:
            resp = requests.post(
                f"{API_BASE}/labels",
                params={
                    **auth,
                    "idBoard": board_id,
                    "name": lbl["name"],
                    "color": lbl["color"],
                },
            )
            resp.raise_for_status()
            label_map[lbl["name"]] = resp.json()["id"]
        return label_map

    def create_lists(self, board_id: str, lists: List[Dict]) -> Dict[str, str]:
        list_map = {}
        for lst in lists:
            params = {
                **auth,
                "idBoard": board_id,
                "name": lst["name"],
                "pos": lst["pos"],
            }
            resp = requests.post(f"{API_BASE}/lists", params=params)
            if not resp.ok:
                print(
                    f"ERROR creating list '{lst['name']}':", resp.status_code, resp.text
                )
            else:
                data = resp.json()
                list_map[lst["name"]] = data["id"]
                print(f"📋 Created list: {lst['name']}")
        return list_map

    def create_card(
        self, list_id: str, name: str, label_ids: List[str], desc: str = ""
    ) -> bool:
        resp = requests.post(
            f"{API_BASE}/cards",
            params={
                **auth,
                "idList": list_id,
                "name": name,
                "idLabels": ",".join(label_ids),
                "desc": desc,
            },
        )
        return resp.ok

    def get_board_lists(self, board_id: str) -> List[Dict]:
        resp = requests.get(f"{API_BASE}/boards/{board_id}/lists", params=auth)
        resp.raise_for_status()
        return resp.json()

    def remove_default_lists(self, board_id: str):
        existing_lists = self.get_board_lists(board_id)
        default_list_names = {"To Do", "Doing", "Done"}

        for lst in existing_lists:
            if lst["name"] in default_list_names:
                self.archive_list(lst["id"])

    def archive_list(self, list_id: str):
        resp = requests.put(
            f"{API_BASE}/lists/{list_id}/closed",
            params={**auth, "value": "true"},
        )
        if resp.ok:
            print(f"🗑️ Removed default list")
        else:
            print(f"⚠️ Could not remove default list: {resp.status_code}")


def main():
    parser = argparse.ArgumentParser(
        description="Create Trello board from markdown checklist"
    )
    parser.add_argument(
        "-f", "--file", default="project_plan.md", help="Markdown file path"
    )
    parser.add_argument("-b", "--board-name", help="Board name")
    parser.add_argument(
        "-d", "--dry-run", action="store_true", help="Show what would be created"
    )
    parser.add_argument("-c", "--config", help="Custom configuration file (JSON)")
    parser.add_argument(
        "-v", "--version", action="version", version=f"Trello Import Tool {__version__}"
    )

    args = parser.parse_args()

    config = None
    if args.config and os.path.exists(args.config):
        with open(args.config, "r") as f:
            config = json.load(f)
    parser_obj = MarkdownParser(args.file)
    categorizer = TaskCategorizer(config)

    # Parse tasks
    print(f"📋 Parsing tasks from {args.file}...")
    tasks = parser_obj.parse()
    print(f"Found {len(tasks)} tasks across {len(parser_obj.sections)} sections")

    # Generate board name with priority order:
    # 1. Command line argument --board-name
    # 2. Configuration file board_name
    # 3. Project title from markdown file
    # 4. Fallback to filename
    board_name = args.board_name
    if not board_name and config and "board_name" in config:
        board_name = config["board_name"]
    if not board_name and parser_obj.project_title:
        board_name = parser_obj.project_title
    if not board_name:
        board_name = f"Project ({os.path.basename(args.file)})"

    if args.dry_run:
        print(f"\n🔍 DRY RUN - Would create board: '{board_name}'")
        print(f"Labels: {[lbl['name'] for lbl in categorizer.config['labels']]}")
        print(f"Lists: {[lst['name'] for lst in categorizer.config['lists']]}")
        print(f"\nTasks breakdown:")

        completed = sum(1 for t in tasks if t["completed"])
        incomplete = len(tasks) - completed

        print(f"✅ Completed: {completed}")
        print(f"⏳ Incomplete: {incomplete}")

        for task in tasks[:5]:
            labels = categorizer.categorize(task)
            target_list = categorizer.determine_list(task)
            status = "✅" if task["completed"] else "⏳"
            print(f"  {status} {task['name']} → {target_list} ({', '.join(labels)})")

        if len(tasks) > 5:
            print(f"  ... and {len(tasks) - 5} more tasks")

        return

    # Create board
    try:
        trello = TrelloAPI()
    except ValueError as e:
        return 1

    print(f"📋 Creating Trello board: '{board_name}'...")
    board_id = trello.create_board(board_name)

    print("📋 Creating labels...")
    label_map = trello.create_labels(board_id, categorizer.config["labels"])

    print("📋 Creating lists...")
    list_map = trello.create_lists(board_id, categorizer.config["lists"])

    print("📋 Creating cards...")
    created_count = 0
    failed_count = 0

    for task in tasks:
        task_labels = categorizer.categorize(task)
        target_list = categorizer.determine_list(task)

        list_id = list_map.get(target_list)
        if not list_id:
            print(f"⚠️ List '{target_list}' not found for task: {task['name']}")
            failed_count += 1
            continue

        label_ids = [label_map[name] for name in task_labels if name in label_map]

        desc_parts = [f"Section: {task['section']}"]
        if task.get("subsection"):
            desc_parts.append(f"Subsection: {task['subsection']}")
        desc_parts.append(f"Line: {task['line']}")
        description = "\n".join(desc_parts)

        if trello.create_card(list_id, task["name"], label_ids, description):
            created_count += 1
        else:
            print(f"❌ Failed to create card: {task['name']}")
            failed_count += 1

    print(f"\n✅ Trello board created successfully!")
    print(f"✅ Summary: {created_count} cards created, {failed_count} failed")
    print(f"📊 Check your Trello dashboard for board: '{board_name}'")


if __name__ == "__main__":
    main()
