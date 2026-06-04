FreeCAD のドキュメントを FCStd ファイルと Python スクリプトとして `projects/` に保存する。

Usage: /freecad-save [doc_name]

## Steps

### 1. ドキュメント名を決定する

- 引数が指定されている場合（例: `/freecad-save CylinderDoc`）、それをドキュメント名として使用する。
- 引数が指定されていない場合、次の Python コードを uv 経由で実行して開いているドキュメント一覧を取得する:
  ```python
  import xmlrpc.client, json
  server = xmlrpc.client.ServerProxy("http://localhost:9875", allow_none=True)
  docs = server.list_documents()
  print(json.dumps(docs))
  ```
  実行コマンド: `cd "C:\Users\jut30\FreeCAD\FreeCAD-MCP"; uv run python -c "<上記コード>"`
  - ドキュメントが1つだけならそれを使用する。
  - 複数ある場合はユーザーに選択を求める。
  - 1つもない場合はエラーを伝える。

### 2. FCStd ファイルを保存する

次のコードをインラインスクリプトとして一時ファイルに書き出し、uv 経由で実行する:

```python
import xmlrpc.client, json
server = xmlrpc.client.ServerProxy("http://localhost:9875", allow_none=True)
doc_name = "{決定したドキュメント名}"
save_path = "C:/Users/jut30/FreeCAD/FreeCAD-MCP/projects/{doc_name}.FCStd"
code = f'import FreeCAD\ndoc = FreeCAD.getDocument("{doc_name}")\nif doc:\n    doc.saveAs("{save_path}")\n    print("saved")\nelse:\n    print("not found")'
result = server.execute_code(code)
print(json.dumps(result, ensure_ascii=False, indent=2))
```

このコードは `projects/{doc_name}.FCStd` に保存する。

### 3. ドキュメントのオブジェクト情報を取得する

次のコードで、ドキュメント内のオブジェクト一覧とプロパティを取得する:

```python
import xmlrpc.client, json
server = xmlrpc.client.ServerProxy("http://localhost:9875", allow_none=True)
objects = server.get_objects("{決定したドキュメント名}")
print(json.dumps(objects, ensure_ascii=False, indent=2))
```

### 4. Python スクリプトを生成・保存する

取得したオブジェクト情報をもとに、FreeCAD MCP の RPC 経由でモデルを再現できる Python スクリプトを生成する。
スクリプトの形式は以下の通り:

```python
"""
FreeCAD MCP - {doc_name} 作成スクリプト
生成日: {YYYY-MM-DD}
"""

import xmlrpc.client

server = xmlrpc.client.ServerProxy("http://localhost:9875", allow_none=True)

# ドキュメントを作成
result = server.create_document("{doc_name}")
print("ドキュメント作成:", result)

# オブジェクトを作成（取得したオブジェクト情報から生成）
obj_data = {
    "Type": "{obj_type}",
    "Name": "{obj_name}",
    "Properties": {
        # 取得したプロパティをここに展開
    },
}
result = server.create_object("{doc_name}", obj_data)
print("{obj_name} 作成:", result)
```

生成したスクリプトを `projects/create_{doc_name}.py` に保存する（Write ツールを使用）。

### 5. 完了を報告する

以下を日本語でユーザーに伝える:
- 保存した FCStd ファイルのパス
- 保存した Python スクリプトのパス
- ドキュメント内に含まれるオブジェクトの概要（名前・種類）
