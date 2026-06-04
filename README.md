# FreeCAD MCP

Claude Desktop から FreeCAD を操作できる MCP サーバーです。

## デモ

### フランジの設計

![demo](./assets/freecad_mcp4.gif)

### トイカーの設計

![demo](./assets/make_toycar4.gif)

### 2D 図面から 3D パーツを設計

#### 入力画像（2D 図面）

![input](./assets/b9-1.png)

#### デモ

![demo](./assets/from_2ddrawing.gif)

会話履歴はこちら:
https://claude.ai/share/7b48fd60-68ba-46fb-bb21-2fbb17399b48

## アドオンのインストール

FreeCAD のアドオンディレクトリは以下の通りです。

| OS | バージョン | パス |
|---|---|---|
| Windows | FreeCAD 1.1 | `%APPDATA%\FreeCAD\v1-1\Mod\` |
| Windows | FreeCAD 1.0 | `%APPDATA%\FreeCAD\Mod\` |
| macOS | FreeCAD 1.1 | `~/Library/Application Support/FreeCAD/v1-1/Mod/` |
| macOS | FreeCAD 1.0 | `~/Library/Application Support/FreeCAD/v1-0/Mod/` |
| Linux (Ubuntu) | — | `~/.FreeCAD/Mod/`（snap の場合: `~/snap/freecad/common/Mod/`） |
| Linux (Debian) | — | `~/.local/share/FreeCAD/Mod` |
| Linux (Arch / CachyOS) | FreeCAD 1.1 | `~/.local/share/FreeCAD/v1-1/Mod/` |

`addon/FreeCADMCP` ディレクトリを上記のアドオンディレクトリにコピーしてください。

```bash
git clone https://github.com/Yaeshio/FreeCAD-MCP-For-YDGA.git
cd FreeCAD-MCP-For-YDGA

# Linux (Ubuntu/Debian)
cp -r addon/FreeCADMCP ~/.FreeCAD/Mod/

# Linux (Arch/CachyOS, FreeCAD 1.1)
mkdir -p ~/.local/share/FreeCAD/v1-1/Mod/
cp -r addon/FreeCADMCP ~/.local/share/FreeCAD/v1-1/Mod/

# macOS (FreeCAD 1.1)
cp -r addon/FreeCADMCP ~/Library/Application\ Support/FreeCAD/v1-1/Mod/
```

```powershell
# Windows (PowerShell) - プロジェクトルートから実行
# FreeCAD 1.1
robocopy addon\FreeCADMCP "$env:APPDATA\FreeCAD\v1-1\Mod\FreeCADMCP" /E /NFL /NDL

# FreeCAD 1.0
robocopy addon\FreeCADMCP "$env:APPDATA\FreeCAD\Mod\FreeCADMCP" /E /NFL /NDL
```

インストール後、FreeCAD を再起動してください。  
ワークベンチ一覧から **「MCP Addon」** を選択すると使用できます。

![workbench_list](./assets/workbench_list.png)

**「FreeCAD MCP」** ツールバーの **「Start RPC Server」** をクリックして RPC サーバーを起動します。

![start_rpc_server](./assets/start_rpc_server.png)

### RPC サーバーの自動起動

デフォルトでは FreeCAD を開くたびに手動で RPC サーバーを起動する必要があります。自動起動を有効にするには:

1. MCP Addon ワークベンチに切り替えてから **「FreeCAD MCP」** メニューを開く
2. **「Auto-Start Server」** にチェックを入れる

設定は `freecad_mcp_settings.json` に保存され、次回以降の FreeCAD 起動時に自動的に RPC サーバーが起動します。  
無効にするには同じメニューの **「Auto-Start Server」** のチェックを外してください。

## Claude Desktop のセットアップ

事前に [uvx](https://docs.astral.sh/uv/guides/tools/) をインストールしてください。

Claude Desktop の設定ファイル `claude_desktop_config.json` を編集します。

**通常ユーザー向け**

```json
{
  "mcpServers": {
    "freecad": {
      "command": "uvx",
      "args": [
        "freecad-mcp"
      ]
    }
  }
}
```

トークンを節約したい場合は `--only-text-feedback` を追加します（スクリーンショットなし）。

```json
{
  "mcpServers": {
    "freecad": {
      "command": "uvx",
      "args": [
        "freecad-mcp",
        "--only-text-feedback"
      ]
    }
  }
}
```

**開発者向け（ローカルクローンを使用）**

```bash
git clone https://github.com/Yaeshio/FreeCAD-MCP-For-YDGA.git
```

```json
{
  "mcpServers": {
    "freecad": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/freecad-mcp/",
        "run",
        "freecad-mcp"
      ]
    }
  }
}
```

## リモート接続

デフォルトでは RPC サーバーは `localhost` のみで待ち受けます。別のマシンの FreeCAD を操作したい場合は以下の手順で設定してください。

### 1. FreeCAD 側でリモート接続を有効化

**「FreeCAD MCP」** ツールバーで:

1. **「Remote Connections」** にチェックを入れる — 次回再起動時に RPC サーバーが `0.0.0.0`（全インターフェース）でバインドされます。セキュリティのため、**「Allowed IPs」** で許可した IP アドレスまたは CIDR サブネットからの接続のみ受け付けます（デフォルト: `127.0.0.1`）。
2. **「Configure Allowed IPs」** をクリックし、許可する IP アドレスまたは CIDR サブネットをカンマ区切りで入力します。例:

   ```
   192.168.1.100, 10.0.0.0/24
   ```

   設定変更後は RPC サーバーを再起動してください。

### 2. MCP サーバーにリモートホストを指定

`--host` フラグに FreeCAD が動作するマシンの IP アドレスまたはホスト名を指定します。

```json
{
  "mcpServers": {
    "freecad": {
      "command": "uvx",
      "args": [
        "freecad-mcp",
        "--host", "192.168.1.100"
      ]
    }
  }
}
```

`--host` の値は起動時に検証されます（有効な IPv4/IPv6 アドレスまたはホスト名が必要）。

## 利用可能なツール

| ツール名 | 説明 |
|---|---|
| `create_document` | FreeCAD に新しいドキュメントを作成する |
| `create_object` | FreeCAD にオブジェクトを作成する |
| `edit_object` | FreeCAD のオブジェクトを編集する |
| `delete_object` | FreeCAD のオブジェクトを削除する |
| `execute_code` | FreeCAD 上で任意の Python コードを実行する |
| `execute_code_async` | GUI に触れない長時間処理を非同期で実行する |
| `insert_part_from_library` | [パーツライブラリ](https://github.com/FreeCAD/FreeCAD-library) からパーツを挿入する |
| `get_view` | アクティブビューのスクリーンショットを取得する |
| `get_objects` | ドキュメント内の全オブジェクト一覧を取得する |
| `get_object` | 指定オブジェクトのプロパティを取得する |
| `get_parts_list` | [パーツライブラリ](https://github.com/FreeCAD/FreeCAD-library) のパーツ一覧を取得する |
| `reload_document` | ドキュメントをディスクから再読み込みする |
| `list_documents` | 開いているドキュメントの一覧を取得する |
| `run_fem_analysis` | CalculiX ソルバーで FEM 解析を実行し、最大 von Mises 応力・最大変位・節点数などの結果を返す。使用例は [`examples/cantilever_fem.py`](examples/cantilever_fem.py) を参照 |

## 上流リポジトリ

[neka-nat/freecad-mcp](https://github.com/neka-nat/freecad-mcp) をフォークしています。
