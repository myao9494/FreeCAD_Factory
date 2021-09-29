# -*- coding: utf-8 -*-
import ptvsd
print("Waiting for debugger attach")
# 5678 is the default attach port in the VS Code debug configurations
ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
ptvsd.wait_for_attach()

import FreeCAD
v1 = FreeCAD.Vector(5,0,0)
v1.normalize()
print (str(v1))
