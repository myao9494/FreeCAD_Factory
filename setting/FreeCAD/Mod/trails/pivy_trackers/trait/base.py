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
Base class for Tracker objects
"""

from ..coin.coin_enums import NodeTypes as Nodes
from ..coin.coin_group import CoinGroup

from ..coin.todo import todo

from ..state.view_state import ViewState
from ..state.mouse_state import MouseState

from .event import Event

class Base():
    """
    Base class for Tracker objects
    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Class statics
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #global view state singleton
    view_state = None

    #global mouse state singleton
    mouse_state = None

    #global reference to the local root node at the top of the entire
    #structure for all trackers.  Typically, this is the 'task-level' root node
    local_root = None

    is_switched = None
    is_separated = None
    switch_first = None

    is_inserted = False

    on_insert_callbacks = []

    @staticmethod
    def init_graph(is_switched=True, is_separated=True, switch_first=True):
        """
        Sets default state for graph generated by CoinGroup
        """
        Base.is_switched = is_switched
        Base.is_separated = is_separated
        Base.switch_first = switch_first

    @staticmethod
    def on_insert():
        """
        Overridable callback triggered after the graph has been inserted
        """

        for _fn in Base.on_insert_callbacks:

            if _fn:
                _fn()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Class Defiintion
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, name, view=None, parent=None, index=-1):
        """
        Constructor
        """

        #name is three parts, delimited by periods ('doc.task.obj')
        #object name is always first
        self.names = name.split('.')[::-1]
        self.name = self.names[0]
        self.type_name = ''

        #pad array to ensure three elements
        if len(self.names) < 3:
            self.names += ['']*(3-len(self.names))

        if not Base.view_state:
            Base.view_state = ViewState(view)

        if not Base.mouse_state:
            Base.mouse_state = MouseState()

        #provide reference to scenegraph root for CoinGroup for default
        #node creation / destruction
        CoinGroup.scenegraph_root = Base.view_state.sg_root

        self.sg_root = Base.view_state.sg_root
        self.callbacks = {}
        self.parent = parent

        self.base = CoinGroup(
            is_separated=Base.is_separated,
            is_switched=Base.is_switched,
            switch_first=Base.switch_first,
            name=f'{self.name}_BASE', parent=parent, index=index)

        self.path_node = None
        self.transform = self.base.add_node(Nodes.TRANSFORM, 'Transform')
        self.base.transform = self.transform

        self.top = self.base.top
        self.root = self.base.root

        #First-created tracker provides the local root node reference
        if not Base.local_root:
            Base.local_root = self.root

        Base.init_graph()

        super().__init__()

    def insert_into_scenegraph(self, verbose=False):
        """
        Insert the base node into the scene graph and trigger notifications
        """

        todo.delay(self._do_insert, verbose)

    def transform_points(self, points, node, parent=None):
        """
        Transform points by the transformation matrix
        points = a list / tuple of 3D coordinates in tuple form
        """

        #no node, use the coordinate node local to this group
        if not node:
            node = self.geometry.coordinate

        if not parent:
            parent = self.view_state.sg_root

        _matrix = self.view_state.get_matrix(node, parent)

        return self.view_state.transform_points(points, _matrix)

    def _do_insert(self, verbose):
        """
        todo.delay callback for node insertion into scenegraph
        """

        Base.view_state.root.addChild(self.base.root)
        Event.set_paths()

        #assign scenegraph root as parent after insertion, rather than
        #when creating the top-level tracker's base coin group.
        self.base.parent = self.view_state.root

        if verbose:
            self.base.dump(self.view_state.root)

            print(
                'triggering {} callbacks...'.format(len(Base.on_insert_callbacks))
            )

        self.on_insert()

        self.is_inserted = True

        if verbose:
            print('{} inserted into scenegraph'.format(self.name))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Wrappers for CoinGroup methods to expose them at the tracker level
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_visibility(self, visible=True):
        """Wrapper"""
        self.base.set_visibility(visible)

    def is_visible(self):
        """Wrapper"""
        return self.base.is_visible()

    def insert_group(self, coin_group):
        """Wrapper"""
        self.base.insert_node(coin_group.root)

    def copy(self):
        """Wrapper"""
        return self.base.copy()

    def finish(self, node=None, parent=None):
        """
        Node destruction / cleanup
        """

        #if Base.view_state:
        #    Base.view_state.finish()
        #    Base.view_state = None

        #if Base.mouse_state:
        #    Base.mouse_state.finish()
        #    Base.mouse_state = None

        self.base.finalize()
        todo.delay(self.sg_root.removeChild, self.root)

Base.init_graph()
