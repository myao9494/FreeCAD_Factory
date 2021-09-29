# -*- coding: utf-8 -*-
#***********************************************************************
#* Copyright (c) 2019 Joel Graff <monograff76@gmail.com>               *
#*                                                                     *
#* This program is free software; you can redistribute it and/or modify*
#* it under the terms of the GNU Lesser General Public License (LGPL)  *
#* as published by the Free Software Foundation; either version 2 of   *
#* the License, or (at your option) any later version.                 *
#* for detail see the LICENCE text file.                               *
#*                                                                     *
#* This program is distributed in the hope that it will be useful,     *
#* but WITHOUT ANY WARRANTY; without even the implied warranty of      *
#* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the       *
#* GNU Library General Public License for more details.                *
#*                                                                     *
#* You should have received a copy of the GNU Library General Public   *
#* License along with this program; if not, write to the Free Software *
#* Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307*
#* USA                                                                 *
#*                                                                     *
#***********************************************************************
"""
Drag tracker for providing drag support to other trackers
"""

from types import SimpleNamespace

from pivy import coin

from ..support.core.singleton import Singleton
from ..support.core.tuple_math import TupleMath

from ..coin.coin_group import CoinGroup
from ..coin.coin_enums import NodeTypes as Nodes
from ..coin.coin_enums import Axis
from ..coin.coin_styles import CoinStyles as Styles

from ..coin import coin_math

from ..trait.base import Base
from ..trait.style import Style
from ..trait.event import Event
from ..trait.pick import Pick
from ..trait.geometry import Geometry

from ..trait.enums import DragStyle

class DragTracker(Base, Style, Event, Pick, Geometry, metaclass=Singleton):
    """
    Drag tracker for providing drag support to other trackers
    """

    def __init__(self, parent):
        """
        Constructor
        """

        #Alter the geometry trait graph before initialization
        Geometry.init_graph(True, True)

        super().__init__('DragTracker', None, parent)

        self.handle_events = False
        self.handle_drag_events = False

        self.drag = CoinGroup(is_switched=True, is_separated=True,
            parent=self.base, name=self.name + '_drag_tracker')

        #build the full drag group graph
        self.drag.full = CoinGroup(is_switched=True, is_separated=True,
            parent=self.drag, name=self.name + '_drag_tracker_full')

        self.drag.full.transform = \
            self.drag.full.add_node(Nodes.TRANSFORM, self.name + '_transform')

        self.drag.full.group =\
            self.drag.full.add_node(Nodes.GROUP, self.name + '_group')

        #build the partial drag group graph
        self.drag.part = CoinGroup(is_switched=True, is_separated=True,
            parent=self.drag, name=self.name + '_drag_tracker_part')

        self.drag.part.coordinate = self.drag.part.add_node(
            Nodes.COORDINATE, self.name + '_coordinate')

        self.drag.part.line = self.drag.part.add_node(
            Nodes.LINE_SET, self.name + '_line')

        #build the no drag group graph
        self.drag.none = CoinGroup(is_switched=True, is_separated=True,
        parent=self.drag, name=self.name + '_drag_tracker_none')

        self.drag.none.group =\
            self.drag.none.add_node(Nodes.GROUP, self.name + 'none_group')

        self.drag.none.transform = self.drag.none.add_node(
            Nodes.TRANSFORM, self.name + 'none_transform'
        )

        self.drag_matrix = None
        self.drag_position = None

        self.drag.none.set_visibility()
        self.drag.part.set_visibility()
        self.drag.full.set_visibility()

        self.drag.set_visibility()
        self.set_visibility()

        self.set_pick_style(False)

        self.constraints = SimpleNamespace(
            axis=None, origin=(0.0, 0.0, 0.0), points=[])

        self.partial = SimpleNamespace(
            coordinates=[],
            transformed=[],
            drag_indices=[],
            group_indices=[]
        )

        self.callbacks = SimpleNamespace(
            before_drag = SimpleNamespace(none=[], partial=[], full=[]),
            on_drag = SimpleNamespace(none=[], partial=[], full=[]),
            after_drag = SimpleNamespace(none=[], partial=[], full=[])
        )

        #initialize the drag line
        self.show_drag_line = True

        self.geometry.line = \
            self.geometry.add_node(Nodes.LINE_SET, self.name + 'drag line')

        self.coin_style = Styles.Style(
            'drag_line', Styles.DASHED, color=Styles.Color.BLUE)

        self.set_style()
        self.geometry.set_visibility(True)

        #enable / disable translation / rotation movements during drag
        self.rotation_enabled = True
        self.translation_enabled = True

        #increment translation / rotation by a fixed value during drag
        #0.0 = free movement
        self.translate_increment = 0.0
        self.rotate_increment = 0.0

        self.proj_origin = ()
        self.lock_axis = ()

        #------------------------
        #drag rotation attributes
        #------------------------

        #cumulative rotation value
        self.rotation = 0.0

        #current bearing of user rotation
        self.angle = 0.0

        #drag center point defined by inheriting class
        self.drag_center = (0.0, 0.0, 0.0)
        self.drag_style = DragStyle.CURSOR
        self.is_rotating = False
        self.update([(0.0, 0.0, 0.0), (0.0, 0.0, 0.0)])

    def set_constraint_geometry(self, axis=None, origin=None, points=None):
        """
        Define geometry which constrains drag movements.
        Axes - a list of one or more 2 or 3-tuples defining axial movement
        Points - a list of one or more 2 or 3-tuples defining linear movement
        """

        self.constraints.axis = None
        self.constraints.points = []

        if axis:

            self.constraints.axis = TupleMath.unit(axis)

        if origin:

            self.constraints.origin = origin

        if points:

            _prev = points[0]

            for _p in points[1:]:

                _delta = TupleMath.subtract(_p, _prev)

                self.constraints.points.append(
                    SimpleNamespace(
                        points=(_prev, _p),
                        delta=_delta,
                        _delta_sq=_delta[0]**2 + _delta[1]**2)
                )

    def get_matrix(self):
        """
        Return the matrix transformation for the full drag geometry
        """

        return self.view_state.get_matrix(self.drag.full.group)

    def insert_no_drag(self, node, cb_before=None, cb_on=None, cb_after=None):
        """
        Subgraph for geometry to be represented during dragging operations
        but otherwist unaffected by dragging
        """

        self.drag.none.insert_node(node, self.drag.none.group)

        _cbs = self.callbacks

        if cb_before:
            _cbs.before_drag.none.append(cb_before)

        if cb_on:
            _cbs.on_drag.none.append(cb_on)

        if cb_after:
            _cbs.after_drag.none.append(cb_after)

    def insert_full_drag(self, node, cb_before=None, cb_on=None, cb_after=None):
        """
        Insert a graph to be fully transformed by dragging

        node - a coin3d group-type node containing drag geometry
        """

        self.drag.full.insert_node(node, self.drag.full.group)

        _cbs = self.callbacks

        if cb_before:
            _cbs.before_drag.full.append(cb_before)

        if cb_on:
            _cbs.on_drag.full.append(cb_on)

        if cb_after:
            _cbs.after_drag.full.append(cb_after)

    def insert_partial_drag(self, coord_node, index_range, indices,
        cb_before=None, cb_on=None, cb_after=None):

        """
        Insert a graph to be partially transformed by dragging

        coord_node - the SoCoordinate node to be added
        index_range - list of two indices indicating first and last coordinate
        indices - the list of indices of coordinates to be dragged
        cb_before, cb_on, cb_after - custom callbacks
        """

        _point = self.drag.part.coordinate.point
        _num = self.drag.part.line.numVertices
        _len = len(_point.getValues())

        #copy the coordinates of the node group to a list
        _pt = coord_node.point
        _coords = [_v.getValue() for _v in _pt.getValues()]
        _xf_coords = _coords[:]

        #only one point indicates no data
        if _len == 1:
            _len = 0

        #get the active view matrix from the node group
        #first call made to clear out previous transform... bug?
        _matrix = self.view_state.get_matrix(self.base.parent)
        _matrix = self.view_state.get_matrix(coord_node)

        #transform coordinates by the transformation active on the node
        _xf_coords = self.view_state.transform_points(_xf_coords, _matrix)

        if not _xf_coords:
            _xf_coords = _coords

        #copy the transformed coordinates back to the original list
        for _i in indices:
            _coords[_i] = _xf_coords[_i]

        #add new coordinates to end of the point SbMFVec3f
        for _i, _v in enumerate(_coords):
            _point.set1Value(_len + _i, _v)

        #store the coordinate that's to be transformed during dragging
        self.partial.drag_indices += [_len + _i for _i in indices]

        _len = len(_num.getValues())

        #-1 indicates unintialized
        if _num.getValues()[0] == -1:
            _len = 0

        #add new vertex number to the NumVertices SbMFInt32 (by reference)
        _num.set1Value(_len, index_range[1] - index_range[0] + 1)

        self.partial.coordinates += _coords
        self.partial.transformed.append(_coords)

        _cbs = self.callbacks

        if cb_before:
            _cbs.before_drag.partial.append(cb_before)

        if cb_on:
            _cbs.on_drag.partial.append(cb_on)

        if cb_after:
            _cbs.after_drag.partial.append(cb_after)

    def set_drag_axis(self, axis):
        """
        Set the lock axis, ensuring it's unit length.
        """

        if axis:
            aixs = TupleMath.unit(axis)

        self.lock_axis = axis

    def begin_drag(self):
        """
        Initialize dragging operation
        """

        if self.partial.drag_indices:

            self.partial.coordinates = [_v.getValue()\
                for _v in self.drag.part.coordinate.point.getValues()]

        self.update([self.drag_center, self.drag_center])

        _matrix = self.get_matrix()
        _cbs = self.callbacks.before_drag

        for _v in [_cbs.none, _cbs.partial, _cbs.full]:
            for _w in _v:
                _w(_matrix)

    def update_drag(self):
        """
        Process mouse movements during dragging
        """

        _coords = [self.drag_center, self.mouse_state.world_position]
        _drag_coords = _coords[1]
        _p_origin = self.constraints.origin
        _prev = None

        #project to the constraining axis
        if self.constraints.axis:

            #store the projected origin...
            if not _p_origin:

                _p_origin = TupleMath.project(_coords[0], self.constraints.axis)

            else:

                _p_origin = TupleMath.project(_p_origin, self.constraints.axis)

            _p_drag = TupleMath.project(_coords[1], self.constraints.axis)

            _drag_coords = TupleMath.add(self.constraints.origin,
                TupleMath.subtract(_p_drag, _p_origin))

            #_delta = TupleMath.project(_coords[1], self.constraints.axis)
            #_delta = TupleMath.subtract(_delta, self.constraints.origin)

            #_drag_coords = TupleMath.add(_coords[0], _delta)

        _proj = []

        #project drag point to constraint geometry, if applicable.
        if self.constraints.points:

            for _p in self.constraints.points:

                _proj = \
                    (_coords[1][0]-_p.points[0]) * _p.delta[0] + (_coords[1][1]-_p.points[1]) * _p.delta[1] / _p._delta_sq

                _dist = TupleMath.manhattan(_coords[1], _proj)

                if _prev is None or _dist < _prev:
                    _drag_coords = _proj
                    _prev=_dist

        #update the transform
        if self.mouse_state.alt_down:
            self.rotate(_coords[0], _drag_coords, self.mouse_state.shift_down)

        else:
            self.translate(
                _coords[0], _drag_coords, self.mouse_state.shift_down)

        if self.show_drag_line and not self.geometry.is_visible():

            #update to prevent incorrect coordinates
            self.update([
                self.mouse_state.world_position,
                self.mouse_state.world_position
            ])

            self.geometry.set_visibility(True)

        _matrix = self.get_matrix()
        _cbs = self.callbacks.on_drag

        self.drag_position = _drag_coords

        for _v in [_cbs.none, _cbs.partial, _cbs.full]:
            for _w in _v:
                _w(_matrix)

    def end_drag(self):
        """
        Terminate dragging operation
        """

        _matrix = self.get_matrix()
        _cbs = self.callbacks.after_drag

        for _v in [_cbs.none, _cbs.partial, _cbs.full]:

            for _w in _v:
                _w(_matrix)

        self.drag_matrix = None

        self.drag.none.group.removeAllChildren()
        self.drag.full.group.removeAllChildren()
        self.drag.part.coordinate.point.setValue((0.0, 0.0, 0.0))
        self.drag.part.line.numVertices.setValue(-1)

        self.partial.drag_indices = []
        self.partial.transformed = []
        self.partial.coordinates = []
        self.full_drag_nodes = []
        self.proj_origin = ()
        self.constraints.axis = None
        self.constraints.points = []
        self.is_rotating = False

        _cbs = self.callbacks

        for _v in [_cbs.before_drag, _cbs.on_drag, _cbs.after_drag]:
            for _w in [_v.none, _v.partial, _v.full]:
                _w = []

        self.callbacks.full = []

        self.geometry.set_visibility(False)

        self.drag.full.set_translation((0.0, 0.0, 0.0))
        self.drag.full.set_rotation(0.0)

        self.drag.none.set_translation((0.0, 0.0, 0.0))
        self.drag.none.set_rotation(0.0)

##########################
## Transformation routines
##########################

    def translate(self, start_coord, end_coord, micro):
        """
        Manage drag geometry translation
        """

        if not self.translation_enabled:
            return

        #exit rotation mode
        if self.is_rotating:

            self.is_rotating = False

            _xlate = self.drag.full.get_translation()
            _world_pos = TupleMath.add(_xlate, self.drag_center)

            self.mouse_state.set_mouse_position(self.view_state, _world_pos)

            return

        #accumulate the movement from the previous mouse position
        _delta = TupleMath.subtract(end_coord, start_coord)

        if self.lock_axis:

            if self.lock_axis[0] == 1.0:
                _delta = (_delta[0], 0.0, 0.0)

            elif self.lock_axis[1] == 1.0:
                _delta = (0.0, _delta[1], 0.0)

            elif self.lock_axis[2] == 1.0:
                _delta = (0.0, 0.0, _delta[2])

            else:
                _delta =\
                    TupleMath.project(_delta[1], self.lock_axis, True)

        #incremental movement
        if self.translate_increment > 0.0:

            _len = int(TupleMath._length(_delta) / self.translate_increment)
            _delta = TupleMath.scale(TupleMath.unit(_delta), _len)

        if not TupleMath.is_zero(_delta):
            self.drag.full.set_translation(_delta)

        if self.show_drag_line:
            self.update([start_coord, end_coord])

        self.transform_partial()

    def rotate(self, center_coord, radius_coord, micro):
        """
        Manage rotation during dragging
        coords - pair of coordinates for the rotation update in tuple form
        """

        #if already rotating get the updated bearing from the center
        if self.is_rotating:

            _center = self.drag.full.get_center()
            _offset = self.drag.full.get_translation()

            _start = TupleMath.add(_center, _offset)
            _vec = TupleMath.subtract(radius_coord, _start)

            _len = TupleMath._length(_vec)

            _angle = coin_math.get_bearing(_vec)

            if self.angle == 0.0:
                self.angle = _angle

            _delta = self.angle - _angle

            if self.rotate_increment > 0.0:

                _d = _delta
                _delta =\
                    int(_delta/self.rotate_increment) * self.rotate_increment

                _angle = self.angle - _delta

            self.rotation += _delta
            self.angle = _angle

            if self.show_drag_line:
                self.update([_start, radius_coord])

        #otherwise, initiate rotation.  Set centerpoint according to values
        #defined by inheriting class
        else:

            self.drag.full.set_center(self.drag_center)
            self.rotation = 0.0
            self.is_rotating = True

        #update the +z axis rotation for the transformation
        self.drag.full.set_rotation (self.rotation, Axis.Z)

        self.transform_partial()

    def transform_partial(self):
        """
        Transform partially-selected geometry
        """

        #iterate partial drag geometry and update
        #zero index is part.coordinate.point index
        _selected = [
            self.partial.coordinates[_v] for _v in self.partial.drag_indices]

        _matrix = self.view_state.get_matrix(
            self.drag.full.group, self.drag.full.top)

        _selected = self.view_state.transform_points(_selected, matrix=_matrix)
        _p = self.partial.coordinates[:]

        for _i, _j in enumerate(self.partial.drag_indices):
            _p[_j] = _selected[_i]
            self.callbacks.on_drag.partial[_i](_selected[_i])

        self.drag.part.coordinate.point.setValues(0, len(_p), _p)

        _offset = 0

        for _i, _j in enumerate(self.partial.drag_indices):

            _k = _j - _offset
            self.partial.transformed[_i][_k] = _selected[_i]
            _offset += len(self.partial.transformed[_i])

    def finish(self):
        """
        Cleanup
        """

        Base.finish(self)
        Style.finish(self)
        Event.finish(self)
        Pick.finish(self)
        Geometry.finish(self)

        self.drag.part.finalize()
        self.drag.full.finalize()
        self.drag.finalize()

        self.partial.coordinates = []
        self.partial.drag_indices = []

        self.coin_style = None
        self.drag_center = None

        Singleton.finish(DragTracker)
