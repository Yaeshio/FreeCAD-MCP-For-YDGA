Generate a design document from Python script changes in a FreeCAD project.

Usage: /freecad-doc [project_name]

## Steps

1. **Determine the project name**
   - If an argument was provided (e.g., `/freecad-doc my_project`), use that as the project name.
   - If no argument, list the directories under `projects/` and ask the user which project to document, or document all projects.

2. **Get the Python script diff**
   - Run: `git diff HEAD~1 -- projects/{project_name}/scripts/`
   - If the output is empty (no committed changes), run: `git diff -- projects/{project_name}/scripts/`
   - If still empty, run: `git diff HEAD -- projects/{project_name}/scripts/` and check if there are any scripts at all with `Get-ChildItem projects/{project_name}/scripts/`
   - If there are scripts but no diff (first commit or untracked), read the script files directly instead.

3. **Analyze the diff and generate the design document**

   Based on the diff (or the full script content if no diff), generate a Markdown design document that includes:

   ### Document structure:
   ```markdown
   # {Project Name} 設計ドキュメント

   **作成日:** {YYYY-MM-DD}
   **ベースコミット:** {git short hash if available}

   ## 変更概要
   何が追加・変更・削除されたかを1〜3文で説明

   ## FreeCADオブジェクト一覧
   作成・変更されたオブジェクトをリスト形式で記載
   各オブジェクトに: 名前、種類、寸法/プロパティ、位置

   ## 設計の意図
   このスクリプトが何を作ろうとしているか、用途や目的

   ## パラメータ・定数
   スクリプト内の重要な数値やパラメータ（変数名と値）

   ## 依存関係・前提条件
   他のオブジェクトへの参照、必要なFreeCAD機能など

   ## 今後の変更候補
   改善可能な点や次のステップ
   ```

4. **Save the document**
   - Determine today's date in YYYYMMDD format.
   - Save the document to: `projects/{project_name}/docs/{YYYYMMDD}_design.md`
   - Create the `docs/` directory if it doesn't exist.
   - If a document for the same date already exists, append a suffix like `_2`, `_3`, etc.

5. **Confirm to the user**
   - Report the path of the saved document.
   - Show a brief summary of what was documented.
