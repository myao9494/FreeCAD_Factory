"""
Fancy routine to smooth zoom the camera
"""

def zoom(ht):
    import FreeCADGui as Gui
    import math
    import FreeCAD as App

    _view = Gui.ActiveDocument.ActiveView
    _camera = _view.getCameraNode()

    _start_pos = App.Vector(_camera.position.getValue().getValue())
    _start_ht = _camera.height.getValue()

    _center = App.Vector()
    _height = ht

    #        if use_bound_box:

    #           _bound_box = self.camera_state['bound box']

    #get the center of the camera, setting the z coordinate positive
    #          _center = Vector(_bound_box.Center)
    #         _center.z = 1.0

    #calculate the camera height = bounding box larger dim + 15%
    #        _height = _bound_box.XMax - _bound_box.XMin
    #       _dy = _bound_box.YMax - _bound_box.YMin

    #            if _dy > _height:
    #               _height = _dy

    #           _height += 0.15 * _height

    _frames = 60.0

    #calculate a total change value
    _pct_chg = abs(_height - _start_ht) / (_height + _start_ht)

    #at 50% change or more, use 60 frames,
    #otherwise scale frames to a minimum of 10 frames
    if _pct_chg < 0.5:
        _frames *= _pct_chg * 2.0

        if _frames < 10.0:
            _frames = 10.0

    #build cosine-based animation curve and reverse
    _steps = [
        math.cos((_i/_frames) * (math.pi/2.0)) * _frames\
            for _i in range(0, int(_frames))
    ]

    _steps = _steps[::-1]

    #calculate position and height deltas for transition loop
    _d_pos = _center - _start_pos
    _d_pos.multiply(1.0 / _frames)

    _d_ht = (_height - _start_ht) / _frames


    for _v in _steps:

        #set the camera
        _view.getCameraNode().position.setValue(
            tuple(_start_pos + (_d_pos * _v))
        )

        _view.getCameraNode().height.setValue(
            _start_ht + (_d_ht * _v)
        )

        Gui.updateGui()
