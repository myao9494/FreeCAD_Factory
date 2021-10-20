# -*- coding: utf-8 -*-

'''
importlib.reload(temp)
temp.hole_hosha()
'''

import FreeCAD as App
import Draft

def hole_hosha(number = 6,Radius=5.0,Height=100.0,z_iti = 100.0):
    """放射状の穴をあけるときに用います

    Args:
        Radius (float, optional): 半径. Defaults to 5.0.
        Height (float, optional): 円柱高さ. Defaults to 100.
        number (int, optional): 放射コピーの数. Defaults to 6.
        z_iti (float, optional): 穴位置（Ｚ座標）. Defaults to 100.
    """
    App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
    App.ActiveDocument.Cylinder.Radius=Radius
    App.ActiveDocument.Cylinder.Height=Height
    App.ActiveDocument.Cylinder.Angle=360.0
    App.ActiveDocument.Cylinder.Placement=App.Placement(App.Vector(0.0,0.0,0.0),App.Rotation(App.Vector(1.0,0.0,0.0),270.0))
    # App.ActiveDocument.recompute()

    App.ActiveDocument.addObject("Part::Cylinder","Cylinder001")
    App.ActiveDocument.Cylinder001.Radius=Radius+1
    App.ActiveDocument.Cylinder001.Height=10.0
    App.ActiveDocument.Cylinder001.Angle=360.0
    App.ActiveDocument.Cylinder001.Placement=App.Placement(App.Vector(0.0,Height,0.0),App.Rotation(App.Vector(1.0,0.0,0.0),270.0))
    App.ActiveDocument.Cylinder001.Label='zaguri_1'
    # App.ActiveDocument.recompute()

    App.ActiveDocument.addObject("Part::Cylinder","Cylinder002")
    App.ActiveDocument.Cylinder002.Radius=Radius+1
    App.ActiveDocument.Cylinder002.Height=10.0
    App.ActiveDocument.Cylinder002.Angle=360.0
    App.ActiveDocument.Cylinder002.Placement=App.Placement(App.Vector(0.0,Height-30.0,0.0),App.Rotation(App.Vector(1.0,0.0,0.0),270.0))
    App.ActiveDocument.Cylinder002.Label='zaguri_2'
    App.ActiveDocument.recompute()

    App.activeDocument().addObject("Part::Compound","Compound")
    App.activeDocument().Compound.Links = [App.activeDocument().Cylinder,App.activeDocument().Cylinder001,App.activeDocument().Cylinder002,]
    App.ActiveDocument.recompute()

    _obj_ = Draft.make_polar_array(App.ActiveDocument.Compound, number=number, angle=360.0, center=App.Vector(0.0, 0.0, 0.0), use_link=True)
    App.ActiveDocument.recompute()
    App.ActiveDocument.Array.Placement=App.Placement(App.Vector(0,0,z_iti), App.Rotation(App.Vector(0,0,1),0), App.Vector(0,0,0))


# Gui.runCommand('Std_DlgMacroRecord',0)
# Gui.Selection.addSelection('Unnamed','Cylinder')
# Gui.Selection.addSelection('Unnamed','Cylinder001')
# Gui.Selection.addSelection('Unnamed','Cylinder002')
# ### Begin command Part_Compound
# App.activeDocument().addObject("Part::Compound","Compound")
# App.activeDocument().Compound.Links = [App.activeDocument().Cylinder,App.activeDocument().Cylinder001,App.activeDocument().Cylinder002,]
# App.ActiveDocument.recompute()
# ### End command Part_Compound
# # Gui.Selection.clearSelection()
# # Gui.Selection.addSelection('Unnamed','Compound')
# Gui.runCommand('Draft_Rotate',0)
# Gui.runCommand('Draft_ArrayTools',1)
# _obj_ = Draft.make_polar_array(App.ActiveDocument.Compound, number=5, angle=360.0, center=FreeCAD.Vector(0.0, 75.0, -0.0), use_link=True)
# # Gui.Selection.addSelection('Unnamed','Array')
# _obj_.Fuse = False
# Draft.autogroup(_obj_)
# App.ActiveDocument.recompute()
# Macro End: C:\Users\M151325\AppData\Roaming\FreeCAD\Macro\kari.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++
