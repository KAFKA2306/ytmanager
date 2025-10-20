# Code Style & Conventions

## Formatting
- Target: Python 3.11
- Indent: 4 spaces
- Line length: 120 characters (Ruff)
- Tool: Ruff formatter and linter

## Naming Conventions
- Modules/functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPERCASE`

## Best Practices
- Pydanticまたはdataclassesで構造化データをモデル化
- 関数は合成可能に保つ
- `config/default.yaml`で設定を管理、リテラルは避ける
- docstringを優先、インラインコメントは意図の明確化のみ
- コメント禁止（ユーザー指示による）
- エラーハンドリング禁止（ユーザー指示による）

## Ruff Configuration
```toml
[tool.ruff]
line-length = 120
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "W"]
ignore = []
```
