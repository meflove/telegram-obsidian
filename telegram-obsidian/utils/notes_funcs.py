import aiofiles
from datetime import datetime
import os

from exceptions import NoteExists
from create_bot import obsidian_path


async def create_note(
    tags=None,
    name=None,
    content=None,
):
    # Если значения равно None, подставляем стандартные данные
    if tags is None:
        tags = ""

    if name is None:
        name = f"Tg note {datetime.now().strftime('%Y.%m.%d %H:%M:%S')}"

    if content is None:
        content = ""

    metadata = f"""---
tags:
  - {"\n  - ".join(tags)}
создал заметку: {datetime.now().strftime("%Y-%m-%d")}
url:
---
"""
    file_path = obsidian_path / "Tg notes" / f"{name}.md"

    if os.path.exists(file_path):
        raise NoteExists(f"Заметка уже существует {name}.md")

    file_path.parent.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(file_path, "w") as f:
        await f.write(metadata)
        await f.write(content)
