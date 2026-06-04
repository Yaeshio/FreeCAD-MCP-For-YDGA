"""
FreeCAD MCP - 円柱モデル作成スクリプト
新しいドキュメント "CylinderDoc" に Part::Cylinder を作成します。
"""

import xmlrpc.client

server = xmlrpc.client.ServerProxy("http://localhost:9875", allow_none=True)

# 新しいドキュメントを作成
result = server.create_document("CylinderDoc")
print("ドキュメント作成:", result)

# 円柱オブジェクトを作成 (半径 15mm、高さ 50mm)
obj_data = {
    "Type": "Part::Cylinder",
    "Name": "Cylinder",
    "Properties": {
        "Height": 50.0,
        "Radius": 15.0,
    },
}
result = server.create_object("CylinderDoc", obj_data)
print("円柱作成:", result)
