"""
Provides capabilities for daily learning from my second brain.
"""
from yaml import safe_load
import random
import markdown
from pathlib import Path

from constants import VAULT_LOCATION


def read_file(path: Path) -> str | None:
    if path.is_file():
        with path.open("r", encoding="utf-8") as file:
            content = file.read()
        return content
    else:
        return None


def extract_metadata(file_content: str | None) -> dict:
    if file_content is None:
        print("No valid file!")
        return {"tags": []}
    elif isinstance(file_content, str) and file_content.startswith("---"):
        metadata_string = file_content.split("---")[1]
        metadata = safe_load(metadata_string)
        if "tags" not in metadata:
            metadata["tags"] = []
        return metadata
    else:
        print("No metadata found!")
        return {"tags": []}


def populate_knowledge_store(root_path: Path) -> dict:
    knowledge_store = {}
    for path in root_path.glob("**/*"):
        if path.is_file():
            content = read_file(path)
            metadata = extract_metadata(content)
            knowledge_store[path] = {
                "content": content,
                "metadata": metadata,
            }
    return knowledge_store


def get_all_tags(store: dict) -> list:
    all_tags = []
    for item in store.values():
        if item.get("metadata"):
            tags = item.get("metadata").get("tags")
            all_tags += tags
    return list(set(all_tags))


def choose_item(store: dict, in_tags: list = None) -> str | None:
    if in_tags:
        filtered_store = {
            k: v
            for k, v in store.items()
            if any(tag in v["metadata"]["tags"] for tag in in_tags)
        }
    else:
        filtered_store = store
    if len(filtered_store) > 0:
        random_key = random.choice(list(filtered_store.keys()))
        return store[random_key].get("content")
    else:
        return None


def convert_to_html(text: str):
    return markdown.markdown(text)


def main():
    knowledge_path = Path(VAULT_LOCATION) / "Sources"

    knowledge_store = populate_knowledge_store(knowledge_path)
    all_tags = get_all_tags(knowledge_store)
    print(sorted(all_tags))

    item = choose_item(knowledge_store, ["career", "politics"])
    print(convert_to_html(item))


if __name__ == "__main__":
    main()
