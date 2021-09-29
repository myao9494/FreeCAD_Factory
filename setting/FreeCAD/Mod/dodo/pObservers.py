#(c) 2019 R. T. LGPL: part of dodo tools w.b. for FreeCAD

__title__="frameTools toolbar"
__author__="oddtopus"
__url__="github.com/oddtopus/dodo"
__license__="LGPL 3"

# import FreeCAD modules
import FreeCAD, FreeCADGui, pCmd
from fObservers import frameObserverPrototype
from uCmd import arrow

pCmd.o1=None
pCmd.port1=None
pCmd.o2=None
pCmd.port2=None
pCmd.arrows1=list()
pCmd.arrows2=list()

class arrow_insert(arrow):
  def __init__(self, name, pype, portNr, scale=100):
    self.stop=False
    self.pype=pype
    self.portDir=pCmd.portsDir(pype)[portNr]
    self.portPos=pCmd.portsPos(pype)[portNr]
    rot=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),self.portDir.negative())
    placement=FreeCAD.Placement(self.portPos,rot)
    super(arrow_insert,self).__init__(pl=placement, scale=[-scale,scale,scale/5], offset=-scale, name=name)
  def pickAction(self,path=None,event=None,arg=None): # sample
    if path:
      for n in path: 
        if str(n.getName())==self.name:
          if self.name[:4]=='obj1': 
            pCmd.port1=int(self.name[-1])
            FreeCAD.Console.PrintMessage('Destination port changed to %i\n' %pCmd.port1)
            if FreeCADGui.Control.activeDialog():
              pass # to understand how to refer to the dialog to update labels
          elif self.name[:4]=='obj2':
            pCmd.port2=int(self.name[-1])
            FreeCAD.Console.PrintMessage('%s %s joined at port %i to %s\n' %(pCmd.o2.PType, pCmd.o2.Label, pCmd.port2,pCmd.o1.Label))
            # move o2
            if type(pCmd.port1)==int and type(pCmd.port2)==int:
              FreeCAD.activeDocument().openTransaction('Join')
              pCmd.join(pCmd.o1,pCmd.port1,pCmd.o2,pCmd.port2)
              FreeCAD.activeDocument().commitTransaction()
            else:
              FreeCAD.Console.PrintError('Port(s) not selected yet\n')
            self.stop=True
    if self.stop:
      for a in pCmd.arrows2:
        a.closeArrow()
      pCmd.arrows2=[]
      pCmd.o2=None
      pCmd.port2=None
      self.stop=False

class joinObserver(frameObserverPrototype): 
  '''
  Mate together the Ports of different Pypes by clicking on
  arrows in the scene-graph.
  '''
  def __init__(self):
    super(joinObserver,self).__init__('Select pypes and ports')
    self.o1=pCmd.o1=None
    pCmd.port1=None
    self.o2=pCmd.o2=None
    pCmd.port2=None
    pCmd.arrows1=list()
    pCmd.arrows2=list()
    #self.o1=pCmd.o1
    #self.o2=pCmd.o2
    FreeCADGui.Selection.clearSelection()
  def goOut(self,info):
    down = (info["State"] == "DOWN")
    k=info['Key']
    if k=="ESCAPE":
      FreeCAD.Console.PrintMessage("I'm escaping.\n")
      for arrow in pCmd.arrows1+pCmd.arrows2:
        arrow.closeArrow()
      self.av.removeEventCallback("SoKeyboardEvent",self.stop)
      FreeCADGui.Selection.removeObserver(self)
  def addSelection(self,doc,obj,sub,pnt):
    sel=FreeCADGui.Selection.getSelection()[0]
    scale=min(sel.Shape.BoundBox.XLength,sel.Shape.BoundBox.YLength,sel.Shape.BoundBox.ZLength)*1.1
    FreeCADGui.Selection.clearSelection()
    if hasattr(sel,'PType') and not pCmd.o1:
      pCmd.o1=self.o1=sel
      for i in range(len(sel.Ports)):
        name='obj1_port'+str(i)
        pCmd.arrows1.append(arrow_insert(name,sel,i,scale))
    else: #if hasattr(sel,'PType') and not pCmd.o2:
      for a in pCmd.arrows2:
        a.closeArrow()
      pCmd.o2=self.o2=sel
      for i in range(len(sel.Ports)):
        name='obj2_port'+str(i)
        a=arrow_insert(name,sel,i,scale)
        a.color.rgb=0,0,.8
        pCmd.arrows2.append(a)
