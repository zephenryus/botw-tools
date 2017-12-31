# TSCB File Format

TSCB files are **t**errain **sc**ene **b**inary files

#### Strings related to TSCB in U-King

```
0x0239fb10
Terrain Scene
Terrain/A/AocField.tscb
MainField
Terrain/A/MainField.tscb
AocField
Terrain/Data/%s.tscb
kInvalid, kFree, kNotInvoked, kInvoked, kDone, kWaiting
BuildResultType
TriggerType
EventType
kInt, kFloat, kString, kWString, kStream
DataType
DataType
kBool, kInt, kFloat, kString, kConst
QueryValueType
kInt, kBool, kFloat, kString, kWString
DataType
kAction, kSwitch, kFork, kJoin, kSubFlow
kArgument, kContainer, kInt, kBool, kFloat, kString, kWString, kIntArray, kBoolArray, kFloatArray, kStringArray, kWStringArray, kActorIdentifier
kFlowchart = 0, kClipEnter = 1, kClipLeave = 2, kOneshot = 3, kNormal = 0, kEnter = 1, kLeave = 2
kSuccess, kInvalidOperation, kResFlowchartNotFound, kEntryPointNotFound
TitleStage
Demo102_0
TitleMenu
ViewerStage
MainField
uking::ViewerStage::draw3D
uking::ViewerStage::draw2D
pViewer
NowLoading
NowLoading_effect1
NowLoading_effect2
NOW LOADING
System/Sead/primitive_renderer_cafe.gsh
System/font/gx2_font/debug_font.gsh
System/font/gx2_font/debug_font.gtx
GraphicsSystem
System/font/gx2_font/debug_font_jis1.gsh
System/font/gx2_font/debug_font_jis1.gtx
System/font/gx2_font/debug_font_jis1_tbl.bin
main
0000001a
起動時間
GameConfig
RootTask
Npc_Zora030
C0
DamageS
Saddle
RunZoraRide
AimHorseLowerBtoF
AimHorseLowerF
AimHorseLowerB
AimHorseLowerWaitB
AimHorseLowerTurnB
0x023a0640

...

0x024d1b00
unforeseen !
おかしい！ [ cur  1st = u : %f, %f @ v : %f, %f | 2nd = u : %f, %f @ v : %f, %f ]
Height
Material
Grass
Water
Height   - Collision
Material - Collision
Grass    - Collision
Water    - Collision
tera::ApertureMaps::updateMap
tera::ApertureMaps::updateMap
tera::ApertureMaps::updateMap
grass
water
extra
height
material
extended
ksys::tera::Scene
マテリアルが読み込まれていないのに Scene::setMaterialUVWInfo が処理されました！
edited
true
type
file_base
area_min_height_water
area_max_height_water
ref_extra
tex_width
area_min_height_ground
area_max_height_ground
【イメージデータ】拡張マップタイプが見つかりません : %s
edited
true
type
file_base
area_min_height_water
area_max_height_water
ref_extra
tex_width
area_min_height_ground
area_max_height_ground
【イメージデータ】拡張マップタイプが見つかりません : %s
scale
x
y
density
ref
width
ratio
slope
name
id
true
scale_range
scale_min
scale_random
【リソース】エキストラデータが見つかりませんでした %s
【データロード】メジャーバージョンの不一致
【データロード】マイナーバージョンの不一致
O
version
scene
world_scale
material_info_array
fabrication_tilling
file_info
material_info
mat_index
tex_index
fabrication_micro
scene_info
height_scale
uv_scale
uvw_info
extra_info_array
area_array
最小／最大高さが取得できないエリアがありました。このエラーが出た場合は斎藤までご連絡をお願いいたします
[tscb 読み込み失敗] シグネチャが違います
[tscb 読み込み失敗] ファイルのバージョンが違います : require %d.%d - exist %d.%d
DegeneracyX
DegeneracyY
NormalFar
NormalNear
NormalMiddle
Dependence
Independence
Normal
DegeneracyX
DegeneracyY
tera::ApertureMaps::updateMap
街道レンダリング：長すぎる分割が見つかりました | %d > %d : num = %f, scale = %f
.%d
grass
water
.hght
.mate
.extm
.mext
extra
height
material
extended
【イメージ】破棄 -> %s
%s/%s
Cache
ksys::tera::ImageResourceMgr
tera::ImageResourceMgr
リクエスト溢れ検出！  対策を実行 ... ： リクエスト処理待ちが無かったため、いったんすべてのリソースを破棄します！
リクエスト溢れ検出！  対策を実行 ... ： リクエストが解放されなかったので、現在のリクエストをすべて破棄します！
%s/
保存失敗！ -> %s
【イメージ】保存 -> %s
【データロード】メモリの確保に失敗しました : %d [align : %d]
.stera
キャンセルされたので再度処理します
ファイルが見つからない
メモリ確保失敗
読み込みが走らなかった
【イメージ】[中断/失敗] : 理由 = %s -> %s
0000444488
【イメージ】読込 -> %s
teraImageResourceMgr
なぜか実行されなかったので再度処理します
【データロード】ランタイムのヒープサイズがファイルサイズより小さい！ - [%s : %d] | %d != %d
【データロード】ファイルが見つからない！ - [%s]
[tera::ImageResourceMgr::procUnloadResidualRequest] 不明なエラーがでました。Error Code = %d
[tera::ImageResourceMgr::procUnloadResidualRequest] ハンドルされていないエラーが出ました。
utility
num.gtx
cage
draw_texture_water_spec
occlusion_query
edit_image_material_add
edit_image_material_ext
conv_modify_map
brush_lower.gtx
brush_upper.gtx
edit_smooth.gtx
edit_spread.gtx
stamp_paste.gtx
draw_texture_height
gen_mipmap_material
edit_image_extended
render_grid
manipulator
aperturemaps_render
edit_matreplace.gtx
stamp_mask_plus.gtx
stamp_manipulate_rotate.gtx
draw_texture_material
gen_normalmap
gen_normalmap_partial
gen_mipmap_height
primitive
edit_image_height_add
edit_image_height_ext
edit_image_height_matbake
edit_mask
edit_path
object_baker_copy
update_random
aperturemaps_route_render
aperturemaps_water_render
shroud_render
debug_tree_render
interact_seed
interact_copy
test2.gtx
test3.gtx
brush_saw.gtx
edit_gradient.gtx
edit_bake.gtx
edit_material.gtx
edit_flow.gtx
draw_texture
draw_texture_partial
draw_texture_composite
draw_texture_water
draw_texture_height_spec
edit_image_material_vert
edit_image_material_fric
edit_image_extra
edit_paste
edit_reflect
soil_erosion
soil_erosion_cross
object_baker_depthfill
object_baker_normalize
render_frame
render_thumbnail_world
render_thumbnail_viewfrustum
aperture_ui_render
dev_mesh
interact_cut
interact_cut_array
interact_reprint
interact_merge
summary_update
test.gtx
brush_normal.gtx
brush_linear.gtx
brush_wave.gtx
edit_add.gtx
edit_sub.gtx
edit_sharpen.gtx
edit_flatten.gtx
edit_matmask.gtx
edit_heightalong.gtx
edit_color.gtx
stamp_mask_minus.gtx
stamp_manipulate_scale.gtx
stamp_manipulate_trans.gtx
path_add.gtx
path_upd.gtx
path_ins.gtx
path_del.gtx
cPosMtx
cTexMtx
cMatMtx
cOffset
cUVInfo
cTexTWS
cHeight
cParam1
cParam2
cParam3
Context
cTexSrc
Cut
%s.%s
cScale
cTrans
cSlice
cColor
cPV[0]
Seed
cTexMatSpecular
cCoeffMatrix[0]
cStepInterpolationParam
cCuringMaskInfo
cTexPasteLinear
cTexImageHeight
cTexPasteHeight
cNormalizeCoeff
cTexOutFlowSkew
cNormalizeParam
cProjViewMtx[0]
TeraCurrentQuad
ViewContext
CurrentQuad
cTargetInfo
cOffsetInfo
cStrokeCoverageTransformSTA
cStrokeCoverageTransformSTB
cSystemInfo
cNoiseParam
cObjectBakeMaskInfo
cTexStrokeCoverageA
cTexStrokeCoverageB
cWorldScale
cRenderingLength[0]
cReflectTransformST
cTexReflect
cScaleTrans
cTexTexture
cGridColor0
cGridColor1
cRenderInfo
cFanPosInfo
cFanAngInfo
cProjMtx[0]
cViewMtx[0]
cShroudInfo
cFrameColor
OuterQuad
LocalInfo
DebugInfo
cTexMatAlbedo
cTexMatNormal
cTexShadowMap
RouteInfo
cTexRefer
cTexCurve
cTexWater
cTexDepth
cTexBrush
cTexFrame
cTexMask1
cTexMask2
cCompositeMaskDst
cTexColor
cTexComposite
cTexPoint
cGroundApertureST
cColorMul
cColorAdd
cTexDecal
cTransform[0]
cTexImage
cBrushPos
cLimitMaskTransformST
cDetailNoiseParam
cMaterialInfo
cGradientMaskInfo
cMaterialParam[0]
cTexLimitMask
cTexNoisePerm
cTexNoiseGrad
cTexNoiseRand
cBrushDensity
cExtensiveTransformST
cTexExtensive
cTexStampMask
cCurveTexInfo
cCurveTexSTMatrix
cTexWaterVelocity
cGridInfo
TeraOuterQuad
TeraLocalInfo
cTeraTexGrass
SystemInfo
OptionInfo
cTexHeight
cTexNormal
cTexMaterial
cTexMaterialLinear
cTexExtended
cTexProjShadow
UIAreaInfo
EditInfo
cTexGrid
cTexNumber
cTexUnitExtended
cTexGuidance
cColorOffset
cTextureInfo
cCompositeMaskSrcMul
cCompositeMaskSrcAdd
cMaterialTexInfo
cMaterialOffset[0]
cTexLinear
cWaterApertureUV
cWaterApertureST
cGroundTexInfo
cTexGround
cReferInfo
cWorldInfo
cPosMtx[0]
cTexMtx[0]
cProj[0]
cView[0]
cFrameInfo
cBrushInfo
cBrushMask
cBrushStroke
cAdjacentMaskTexture
cNoiseScaleParam
cDistortNoiseParam
cMaterialBakeParam
cColorInfo
cAdditionalParam
cTexMaterialBake
cBaseTransformST
cTexBase
cStampMaskInfo
cTexPasteNearest
cTexCuringMask
cReferCoordStart
cReferCoordEnd
cRouteInfo
cOriginalTransformST
cReflectInfo
cEditValue
cMaskTransformST
cTexOriginal
cTexMask
cSimulationCoeff
cTexTerrainWaterSediment
cTexOutFlowCross
cTexWork
cMaterialInfo[0]
cTexAlbedo
cTexRandom
cWorldMtx[0]
cModelMtx[0]
cPVWMtx[0]
cMainColor
TeraSystemInfo
cTeraTexHeight
cTeraTexNormal
tera_common
tera_develop
tera_debug
tera_grass
マテリアルの対応アトリビュートが見つかりません -> No : %d | ファイル : %s | アトリビュート(Main) : %s | アトリビュート(Sub) : %s
[tera::Water::setUpAttributeTable] マテリアルの対応アトリビュートが見つかりません -> No : %d | ファイル : %s | アトリビュート(Main) : %s | アトリビュート(Sub) : %s
マテリアルの対応アトリビュートが見つかりません -> No : %d | ファイル : %s | アトリビュート(Main) : %s | アトリビュート(Sub) : %s
ksys::tera::ResourceHolder
vege.bvege
tera::update_grid
tera::update_frame
【リソース】マテリアルが見つかりません -> %s
MaterialAlb
MaterialCmb
TeraTerrain
OpaqueNear
【リソース】マテリアル用モデルデータが見つかりません -> %s
【リソース】マテリアルテクスチャが見つかりません -> %s
_a0
_n0
Translucent
tera_height
tera_normal
OpaqueFar
tera_material
OpaqueNear
OpaqueMiddle
tera_material_linear
tera_water
_p0
TeraTerrain
【リソース】マテリアル用モデルデータが見つかりません -> %s
OpaqueNear
OpaqueMiddle
OpaqueFar
Translucent
group
name
file
array_index
attribute
attribute_sub
_a0
_n0
ZOnly
tera_height
tera_normal
tera_material
tera_material_linear
tera_water
_p0
TeraTerrain
【リソース】マテリアル用モデルデータが見つかりません -> %s
ZOnly
Opaque
【リソース】マテリアルが見つかりません -> %s
MaterialAlb
MaterialCmb
TeraRoute
【リソース】マテリアル用モデルデータが見つかりません -> %s
【リソース】マテリアルテクスチャが見つかりません -> %s
Opaque
Translucent
tera_height
tera_refer
tera_curve
_p0
TeraRoute
【リソース】マテリアル用モデルデータが見つかりません -> %s
Opaque
Translucent
name
file
array_index
attribute
attribute_sub
Blade1
Cross1
Cover1
【リソース】マテリアルが見つかりません -> %s
TeraGrass
GrassCrossAlb
GrassCoverAlb
GrassAlb
【リソース】マテリアル用モデルデータが見つかりません -> %s
【リソース】草テクスチャが見つかりません -> %s
_n0
_a0
Blade1
Blade2
Cross1
Cross2
Cover1
Cover2
Translucent
grass_color
grass_mow
grass_lie
grass_wind_swell
grass_mow_wide
grass_summary0
grass_summary1
grass_cover_perp
_p0
_n0
_t0
_u0
TeraGrass
【リソース】マテリアル用モデルデータが見つかりません -> %s
DrawBlade1__Blade1
DrawBlade2__Blade2
DrawCover1__Cover1
DrawCover2__Cover2
DrawCross1__Cross1
DrawCross2__Cross2
Xlu__Translucent
name
【リソース】マテリアルが見つかりません -> %s
TeraFlower
【リソース】マテリアル用モデルデータが見つかりません -> %s
【リソース】草テクスチャが見つかりません -> %s
Petal
Normal
Long
Cross
FallenLeaves
Stone
Shell
Chips
FlowerPetalAlb
FlowerNormalAlb
FlowerLongAlb
FlowerCrossAlb
FlowerFallenLeavesAlb
FlowerStoneAlb
FlowerShellAlb
FlowerChipsAlb
TeraFlower
【リソース】マテリアル用モデルデータが見つかりません -> %s
_n0
【リソース】マテリアルが見つかりません -> %s
Translucent
TeraWater
WaterAlb
WaterNrm
WaterEmm
【リソース】水モデルデータが見つかりません -> %s
【リソース】マテリアルテクスチャが見つかりません -> %s
Translucent
tera_height
tera_water
_p0
TeraWater
【リソース】マテリアル用モデルデータが見つかりません -> %s
Translucent
group
name
file
array_index
attribute
attribute_sub
Tree0
Tree1
【リソース】マテリアルが見つかりません -> %s
Tree0NrmTrs
Tree1NrmTrs
TeraTree
Tree0Alb
TreeDitherMask
Tree1Alb
【リソース】マテリアル用モデルデータが見つかりません -> %s
【リソース】ビルボード樹木テクスチャが見つかりません -> %s
Tree0
Tree1
Xlu0
a0
n0
TeraTree
【リソース】マテリアル用モデルデータが見つかりません -> %s
```
