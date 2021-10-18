# ***************************************************************************
# *   Copyright (c) 2021 myao9494                                           *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# ***************************************************************************

"""Initialization of the Mine workbench (graphical interface)."""

import os
import FreeCAD
import FreeCADGui
class MineWorkbench(FreeCADGui.Workbench):
    """The Mine workbench definition."""

    def __init__(self):
        self.__class__.Icon = os.path.join(FreeCAD.getUserAppDataDir() , "Mod","Mine","Resources","Icons","ponpoko.svg")
        self.__class__.ToolTip  = "This is my freecad env !!"
        self.__class__.MenuText = "Mine"

    def Initialize(self):
        """When the workbench is first loaded."""

        def QT_TRANSLATE_NOOP(context, text):
            return text

        import Draft_rc
        import DraftTools
        import DraftGui
        from draftguitools import gui_circulararray
        from draftguitools import gui_polararray
        from draftguitools import gui_orthoarray
        from draftguitools import gui_arrays
        import Design456_SelectionGate as SelGate

        # Set up Draft command lists
        import draftutils.init_tools as it
        self.draft_drawing_commands = it.get_draft_drawing_commands()
        self.draft_annotation_commands = it.get_draft_annotation_commands()
        self.draft_modification_commands = it.get_draft_modification_commands()
        self.draft_context_commands = it.get_draft_context_commands()
        self.draft_line_commands = it.get_draft_line_commands()
        self.draft_utility_commands = it.get_draft_utility_commands()

        # Set up toolbars
        self.appendToolbar(QT_TRANSLATE_NOOP("Draft", "Draft creation tools"), self.draft_drawing_commands)
        self.appendToolbar(QT_TRANSLATE_NOOP("Draft", "Draft annotation tools"), self.draft_annotation_commands)
        self.appendToolbar(QT_TRANSLATE_NOOP("Draft", "Draft modification tools"), self.draft_modification_commands)

        self.appendMenu([QT_TRANSLATE_NOOP("Mine", "&Draft"),
                         QT_TRANSLATE_NOOP("Mine", "Creation")],
                        self.draft_drawing_commands)
        self.appendMenu([QT_TRANSLATE_NOOP("Mine", "&Draft"),
                         QT_TRANSLATE_NOOP("Mine", "Annotation")],
                        self.draft_annotation_commands)
        self.appendMenu([QT_TRANSLATE_NOOP("Mine", "&Draft"),
                         QT_TRANSLATE_NOOP("Mine", "Modification")],
                        self.draft_modification_commands)
        self.appendMenu([QT_TRANSLATE_NOOP("Mine", "&Draft"),
                         QT_TRANSLATE_NOOP("Mine", "Utilities")],
                        self.draft_utility_commands
                        + self.draft_context_commands)
        self.appendToolbar("Selection Mode",SelGate.Design456_SelectionGate.list)

        FreeCAD.Console.PrintLog('Loading Mine workbench, done.\n')

    def Activated(self):
        """When entering the workbench."""
        if hasattr(FreeCADGui, "draftToolBar"):
            FreeCADGui.draftToolBar.Activated()
        if hasattr(FreeCADGui, "Snapper"):
            FreeCADGui.Snapper.show()
        FreeCAD.Console.PrintLog("Mine workbench activated.\n")

    def Deactivated(self):
        """When leaving the workbench."""
        if hasattr(FreeCADGui, "draftToolBar"):
            FreeCADGui.draftToolBar.Deactivated()
        if hasattr(FreeCADGui, "Snapper"):
            FreeCADGui.Snapper.hide()
        FreeCAD.Console.PrintLog("Mine workbench deactivated.\n")

    def ContextMenu(self, recipient):
        """Define an optional custom context menu."""
        self.appendContextMenu("Utilities", self.draft_context_commands)

    def GetClassName(self):
        """Type of workbench."""
        return "Gui::PythonWorkbench"

FreeCADGui.addWorkbench(MineWorkbench)