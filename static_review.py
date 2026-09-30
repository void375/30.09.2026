"""Узкий учебный анализатор AST. Не заменяет полноценный линтер."""
import ast
import sys
from pathlib import Path

path = Path(sys.argv[1] if len(sys.argv) > 1 else "helpdesk.py")
tree = ast.parse(path.read_text(encoding="utf-8"))
used = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
count = 0
for node in ast.walk(tree):
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        for item in node.names:
            name = item.asname or item.name.split(".")[0]
            if name not in used:
                print(f"{path}:{node.lineno}: W001 импорт {name} возможно не используется")
                count += 1
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        for default in [*node.args.defaults, *node.args.kw_defaults]:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                print(f"{path}:{node.lineno}: W002 изменяемое значение аргумента по умолчанию в {node.name}")
                count += 1
print(f"Предупреждений: {count}. Правила W001 и W002 требуют проверки человеком.")
