import os
import asyncio
import sys
from create_bot import obsidian_path


class Tree:
    def __init__(self, limit=None, root_name=""):
        self.dirCount = 0
        self.fileCount = 0
        self.limit = limit
        self.root_name = root_name

    def summary(self):
        return f"{self.dirCount} directories, {self.fileCount} files"

    async def walk(self, directory, prefix=""):
        if not self.root_name:
            self.root_name = os.path.basename(directory.rstrip(os.sep))

        try:
            filepaths = await asyncio.to_thread(os.listdir, directory)
        except Exception as e:
            return [f"{prefix}[error: {str(e)}]"]

        filepaths = sorted([f for f in filepaths if not f.startswith(".")])
        entries = []
        total = len(filepaths)

        for index, name in enumerate(filepaths):
            is_last = index == total - 1
            absolute = os.path.join(directory, name)

            try:
                is_dir = await asyncio.to_thread(os.path.isdir, absolute)
            except Exception as e:
                self.fileCount += 1
                entries.append(
                    f"{prefix}{'└── ' if is_last else '├── '}{name} [error: {e}]"
                )
                continue

            if is_dir:
                if self.limit is not None and self.dirCount >= self.limit:
                    entries.append(
                        f"{prefix}{'└── ' if is_last else '├── '}{name} [dir: omitted due to limit]"
                    )
                else:
                    self.dirCount += 1
                    entries.append(f"{prefix}{'└── ' if is_last else '├── '}{name}")

                    if self.limit is not None and self.dirCount >= self.limit:
                        entries.append(
                            f"{prefix}{'    ' if is_last else '│   '}[content omitted due to limit]"
                        )
                    else:
                        new_prefix = prefix + ("    " if is_last else "│   ")
                        try:
                            child_entries = await self.walk(absolute, new_prefix)
                            entries.extend(child_entries)
                        except Exception as e:
                            entries.append(
                                f"{prefix}{'    ' if is_last else '│   '}[error: {e}]"
                            )
            else:
                self.fileCount += 1
                entries.append(f"{prefix}{'└── ' if is_last else '├── '}{name}")

        return entries


async def list_notes_tree():
    vault_path = str(obsidian_path)
    prefix = vault_path.split("/")[-1]

    tree = Tree(limit=None, root_name=prefix)

    root_entry = [tree.root_name] if tree.root_name else []
    child_entries = await tree.walk(vault_path)
    all_entries = root_entry + child_entries

    return "\n".join(all_entries)
