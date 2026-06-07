"""
FreeCAD MCP - SN_721 作成スクリプト
生成日: 2026-06-07

船体中央断面モデル (SN_721) の構造を FreeCAD MCP RPC 経由で再現するスクリプト。

注意: Sketcher オブジェクト内の B-スプライン曲線・拘束データは RPC API 経由では
完全な再現が困難なため、アタッチメント情報と配置のみを復元します。
スケッチの詳細形状は FCStd ファイル (projects/SN_721.FCStd) から読み込んでください。

オブジェクト構成:
  - Part (App::Part) : パーツコンテナ
  - Sketch          : 基準スケッチ（側面断面ライン、XZ平面上）
  - DatumPlane      : Sketch/Vertex7 を基準とした平行移動基準面
  - DatumPlane001   : Sketch/Vertex8 を基準とした平行移動基準面
  - Sketch001       : DatumPlane001 上のスケッチ（横断面 下段）
  - Sketch002       : DatumPlane 上のスケッチ（横断面 上段）
  - DatumPoint      : Sketch002/Vertex13 から生成した基準点
  - DatumPlane002   : DatumPoint を基準とした YZ 面
  - Sketch003       : DatumPlane002 上のスケッチ（縦断面 端部）
  - DatumPlane003   : Sketch/Edge9 に法線方向の基準面
  - Sketch004       : DatumPlane003 上のスケッチ（B-スプライン断面）
  - DatumPoint001   : Sketch002/Vertex7 から生成した基準点
  - DatumPlane004   : DatumPoint001 を基準とした YZ 面
  - Sketch005       : DatumPlane004 上のスケッチ（縦断面 中間）
  - DatumPoint002   : Sketch004/Vertex11 から生成した基準点
  - DatumPlane005   : DatumPoint002 を基準とした YZ 面
  - Sketch006       : DatumPlane005 上のスケッチ（縦断面 内側、完全拘束済み）
  - Surface         : GeomFillSurface（Sketch001〜003のエッジで生成）
  - Surface001      : Filling サーフェス（上面）
  - Surface002      : Filling サーフェス（下面）
"""

import xmlrpc.client

server = xmlrpc.client.ServerProxy("http://localhost:9875", allow_none=True)

# ────────────────────────────────────────────
# 1. ドキュメントを作成
# ────────────────────────────────────────────
result = server.create_document("SN_721")
print("ドキュメント作成:", result)

# ────────────────────────────────────────────
# 2. Part コンテナを作成
# ────────────────────────────────────────────
code = """
import FreeCAD
doc = FreeCAD.getDocument("SN_721")
part = doc.addObject("App::Part", "Part")
part.Label = "Part"
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("Part 作成:", result)

# ────────────────────────────────────────────
# 3. 基準スケッチ (Sketch) を作成
#    MapMode: Deactivated  Placement: Pos=(0,0,0) YPR=(0,0,90)
#    ※ スケッチ内部の形状は FCStd ファイルから復元してください
# ────────────────────────────────────────────
code = """
import FreeCAD
import Sketcher
doc = FreeCAD.getDocument("SN_721")
sk = doc.addObject("Sketcher::SketchObject", "Sketch")
sk.Label = "Sketch"
sk.MapMode = "Deactivated"
import FreeCAD as App
sk.Placement = App.Placement(
    App.Vector(0, 0, 0),
    App.Rotation(App.Vector(0, 0, 1), 90)
)
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("Sketch 作成:", result)

# ────────────────────────────────────────────
# 4. DatumPlane (Sketch/Vertex7 からの Translate)
#    Placement: Pos=(332.741, 0, 67.4334)
# ────────────────────────────────────────────
code = """
import FreeCAD
doc = FreeCAD.getDocument("SN_721")
dp = doc.addObject("Part::DatumPlane", "DatumPlane")
dp.Label = "DatumPlane"
sk = doc.getObject("Sketch")
dp.AttachmentSupport = [(sk, ("Vertex7",))]
dp.MapMode = "Translate"
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("DatumPlane 作成:", result)

# ────────────────────────────────────────────
# 5. DatumPlane001 (Sketch/Vertex8 からの Translate)
#    Placement: Pos=(332.741, 0, 54.4334)
# ────────────────────────────────────────────
code = """
import FreeCAD
doc = FreeCAD.getDocument("SN_721")
dp = doc.addObject("Part::DatumPlane", "DatumPlane001")
dp.Label = "DatumPlane001"
sk = doc.getObject("Sketch")
dp.AttachmentSupport = [(sk, ("Vertex8",))]
dp.MapMode = "Translate"
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("DatumPlane001 作成:", result)

# ────────────────────────────────────────────
# 6. Sketch001 (DatumPlane001 上、FlatFace)
#    Placement: Pos=(332.741, 0, 54.4334)
# ────────────────────────────────────────────
code = """
import FreeCAD
import Sketcher
doc = FreeCAD.getDocument("SN_721")
sk = doc.addObject("Sketcher::SketchObject", "Sketch001")
sk.Label = "Sketch001"
dp = doc.getObject("DatumPlane001")
sk.AttachmentSupport = [(dp, ("",))]
sk.MapMode = "FlatFace"
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("Sketch001 作成:", result)

# ────────────────────────────────────────────
# 7. Sketch002 (DatumPlane 上、FlatFace)
#    Placement: Pos=(332.741, 0, 67.4334)
# ────────────────────────────────────────────
code = """
import FreeCAD
import Sketcher
doc = FreeCAD.getDocument("SN_721")
sk = doc.addObject("Sketcher::SketchObject", "Sketch002")
sk.Label = "Sketch002"
dp = doc.getObject("DatumPlane")
sk.AttachmentSupport = [(dp, ("",))]
sk.MapMode = "FlatFace"
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("Sketch002 作成:", result)

# ────────────────────────────────────────────
# 8. DatumPoint (Sketch002/Vertex13 から CenterOfMass)
#    Placement: Pos=(348.741, 0, 67.4334)
# ────────────────────────────────────────────
code = """
import FreeCAD
doc = FreeCAD.getDocument("SN_721")
dpt = doc.addObject("Part::DatumPoint", "DatumPoint")
dpt.Label = "DatumPoint"
sk = doc.getObject("Sketch002")
dpt.AttachmentSupport = [(sk, ("Vertex13",))]
dpt.MapMode = "CenterOfMass"
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("DatumPoint 作成:", result)

# ────────────────────────────────────────────
# 9. DatumPlane002 (DatumPoint を基準とした ObjectYZ)
#    Placement: Pos=(348.741, 0, 67.4334) YPR=(90, 0, 90)
# ────────────────────────────────────────────
code = """
import FreeCAD
doc = FreeCAD.getDocument("SN_721")
dp = doc.addObject("Part::DatumPlane", "DatumPlane002")
dp.Label = "DatumPlane002"
dpt = doc.getObject("DatumPoint")
dp.AttachmentSupport = [(dpt, ("",))]
dp.MapMode = "ObjectYZ"
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("DatumPlane002 作成:", result)

# ────────────────────────────────────────────
# 10. Sketch003 (DatumPlane002 上、FlatFace)
#     Placement: Pos=(348.741, 0, 67.4334) YPR=(90, 0, 90)
# ────────────────────────────────────────────
code = """
import FreeCAD
import Sketcher
doc = FreeCAD.getDocument("SN_721")
sk = doc.addObject("Sketcher::SketchObject", "Sketch003")
sk.Label = "Sketch003"
dp = doc.getObject("DatumPlane002")
sk.AttachmentSupport = [(dp, ("",))]
sk.MapMode = "FlatFace"
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("Sketch003 作成:", result)

# ────────────────────────────────────────────
# 11. DatumPlane003 (Sketch/Edge9 に法線、NormalToEdge)
#     Placement: Pos=(312.741, 0, 61.4334)
# ────────────────────────────────────────────
code = """
import FreeCAD
doc = FreeCAD.getDocument("SN_721")
dp = doc.addObject("Part::DatumPlane", "DatumPlane003")
dp.Label = "DatumPlane003"
sk = doc.getObject("Sketch")
dp.AttachmentSupport = [(sk, ("Edge9",))]
dp.MapMode = "NormalToEdge"
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("DatumPlane003 作成:", result)

# ────────────────────────────────────────────
# 12. Sketch004 (DatumPlane003 上、FlatFace)
#     Placement: Pos=(312.741, 0, 61.4334)
#     B-スプライン断面形状を含む（FCStd から復元）
# ────────────────────────────────────────────
code = """
import FreeCAD
import Sketcher
doc = FreeCAD.getDocument("SN_721")
sk = doc.addObject("Sketcher::SketchObject", "Sketch004")
sk.Label = "Sketch004"
dp = doc.getObject("DatumPlane003")
sk.AttachmentSupport = [(dp, ("",))]
sk.MapMode = "FlatFace"
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("Sketch004 作成:", result)

# ────────────────────────────────────────────
# 13. DatumPoint001 (Sketch002/Vertex7 から CenterOfMass)
#     Placement: Pos=(332.741, 0, 67.4334)
# ────────────────────────────────────────────
code = """
import FreeCAD
doc = FreeCAD.getDocument("SN_721")
dpt = doc.addObject("Part::DatumPoint", "DatumPoint001")
dpt.Label = "DatumPoint001"
sk = doc.getObject("Sketch002")
dpt.AttachmentSupport = [(sk, ("Vertex7",))]
dpt.MapMode = "CenterOfMass"
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("DatumPoint001 作成:", result)

# ────────────────────────────────────────────
# 14. DatumPlane004 (DatumPoint001 を基準とした ObjectYZ)
#     Placement: Pos=(332.741, 0, 67.4334) YPR=(90, 0, 90)
# ────────────────────────────────────────────
code = """
import FreeCAD
doc = FreeCAD.getDocument("SN_721")
dp = doc.addObject("Part::DatumPlane", "DatumPlane004")
dp.Label = "DatumPlane004"
dpt = doc.getObject("DatumPoint001")
dp.AttachmentSupport = [(dpt, ("",))]
dp.MapMode = "ObjectYZ"
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("DatumPlane004 作成:", result)

# ────────────────────────────────────────────
# 15. Sketch005 (DatumPlane004 上、FlatFace)
#     Placement: Pos=(332.741, 0, 67.4334) YPR=(90, 0, 90)
# ────────────────────────────────────────────
code = """
import FreeCAD
import Sketcher
doc = FreeCAD.getDocument("SN_721")
sk = doc.addObject("Sketcher::SketchObject", "Sketch005")
sk.Label = "Sketch005"
dp = doc.getObject("DatumPlane004")
sk.AttachmentSupport = [(dp, ("",))]
sk.MapMode = "FlatFace"
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("Sketch005 作成:", result)

# ────────────────────────────────────────────
# 16. DatumPoint002 (Sketch004/Vertex11 から CenterOfMass)
#     Placement: Pos=(312.741, 0, 61.4334)
# ────────────────────────────────────────────
code = """
import FreeCAD
doc = FreeCAD.getDocument("SN_721")
dpt = doc.addObject("Part::DatumPoint", "DatumPoint002")
dpt.Label = "DatumPoint002"
sk = doc.getObject("Sketch004")
dpt.AttachmentSupport = [(sk, ("Vertex11",))]
dpt.MapMode = "CenterOfMass"
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("DatumPoint002 作成:", result)

# ────────────────────────────────────────────
# 17. DatumPlane005 (DatumPoint002 を基準とした ObjectYZ)
#     Placement: Pos=(312.741, 0, 61.4334) YPR=(90, 0, 90)
# ────────────────────────────────────────────
code = """
import FreeCAD
doc = FreeCAD.getDocument("SN_721")
dp = doc.addObject("Part::DatumPlane", "DatumPlane005")
dp.Label = "DatumPlane005"
dpt = doc.getObject("DatumPoint002")
dp.AttachmentSupport = [(dpt, ("",))]
dp.MapMode = "ObjectYZ"
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("DatumPlane005 作成:", result)

# ────────────────────────────────────────────
# 18. Sketch006 (DatumPlane005 上、FlatFace、完全拘束済み)
#     Placement: Pos=(312.741, 0, 61.4334) YPR=(90, 0, 90)
#     形状: Line segment (-17,0,0)→(-17,-7,0)
#     拘束: Coincident×2 (Sketch005/Vertex2, Sketch004/Vertex1)
# ────────────────────────────────────────────
code = """
import FreeCAD
import Sketcher
import Part
doc = FreeCAD.getDocument("SN_721")
sk = doc.addObject("Sketcher::SketchObject", "Sketch006")
sk.Label = "Sketch006"
dp = doc.getObject("DatumPlane005")
sk.AttachmentSupport = [(dp, ("",))]
sk.MapMode = "FlatFace"
doc.recompute()

# 直線ジオメトリを追加
sk.addGeometry(Part.LineSegment(
    FreeCAD.Vector(-17, 0, 0),
    FreeCAD.Vector(-17, -7, 0)
), False)

# 外部ジオメトリ参照 (拘束のための参照点)
sk5 = doc.getObject("Sketch005")
sk4 = doc.getObject("Sketch004")
sk.addExternal(sk5.Name, "Vertex2")
sk.addExternal(sk4.Name, "Vertex1")

doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("Sketch006 作成:", result)

# ────────────────────────────────────────────
# 19. Surface (GeomFillSurface)
#     境界: Sketch003/Edge3, Sketch002/Edge5, Sketch001/Edge3, Sketch001/Edge1
# ────────────────────────────────────────────
code = """
import FreeCAD
doc = FreeCAD.getDocument("SN_721")
sf = doc.addObject("Surface::GeomFillSurface", "Surface")
sf.Label = "Surface"
sk1 = doc.getObject("Sketch001")
sk2 = doc.getObject("Sketch002")
sk3 = doc.getObject("Sketch003")
sf.BoundaryList = [
    (sk3, ("Edge3",)),
    (sk2, ("Edge5",)),
    (sk1, ("Edge3",)),
    (sk1, ("Edge1",)),
]
sf.FillType = "Stretched"
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("Surface 作成:", result)

# ────────────────────────────────────────────
# 20. Surface001 (Filling サーフェス - 上面)
#     境界: Surface/Edge3, Sketch005/Edge2, Sketch006/Edge1+2, Sketch003/Edge2
# ────────────────────────────────────────────
code = """
import FreeCAD
doc = FreeCAD.getDocument("SN_721")
sf = doc.addObject("Surface::Filling", "Surface001")
sf.Label = "Surface001"
surf = doc.getObject("Surface")
sk3 = doc.getObject("Sketch003")
sk5 = doc.getObject("Sketch005")
sk6 = doc.getObject("Sketch006")
sf.BoundaryEdges = [
    (surf, ("Edge3",)),
    (sk5,  ("Edge2",)),
    (sk6,  ("Edge1", "Edge2")),
    (sk3,  ("Edge2",)),
]
sf.BoundaryOrder = [0, 0, 0, 0, 0]
sf.Degree = 3
sf.MaximumDegree = 8
sf.MaximumSegments = 9
sf.Iterations = 2
sf.PointsOnCurve = 15
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("Surface001 作成:", result)

# ────────────────────────────────────────────
# 21. Surface002 (Filling サーフェス - 下面)
#     境界: Sketch004/Edge1, Sketch006/Edge2, Surface/Edge4, Sketch001/Edge1
# ────────────────────────────────────────────
code = """
import FreeCAD
doc = FreeCAD.getDocument("SN_721")
sf = doc.addObject("Surface::Filling", "Surface002")
sf.Label = "Surface002"
surf = doc.getObject("Surface")
sk1 = doc.getObject("Sketch001")
sk4 = doc.getObject("Sketch004")
sk6 = doc.getObject("Sketch006")
sf.BoundaryEdges = [
    (sk4,  ("Edge1",)),
    (sk6,  ("Edge2",)),
    (surf, ("Edge4",)),
    (sk1,  ("Edge1",)),
]
sf.BoundaryOrder = [0, 0, 0, 0]
sf.Degree = 3
sf.MaximumDegree = 8
sf.MaximumSegments = 9
sf.Iterations = 2
sf.PointsOnCurve = 15
doc.recompute()
print("ok")
"""
result = server.execute_code(code)
print("Surface002 作成:", result)

print("\n=== SN_721 モデル構造の再現が完了しました ===")
print("注意: Sketch の詳細形状（B-スプライン、拘束）は projects/SN_721.FCStd から読み込んでください")
