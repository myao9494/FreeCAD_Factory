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
Provides SoFCSelection support for Tracker classes
"""

from pivy import coin

from ..coin.coin_styles import CoinStyles

class Select():
    """
    Provides SoFCSelection support for Tracker classes
    """

    #Base, Style, Event, and Geometry prototypes
    name = None
    names = []
    base = None
    mouse_state = None
    coin_style = None
    event = None

    def set_style(self, style=None, draw=None, color=None):
        """prototype"""; pass

    #geometry prototypes for updating trackers after drag operations
    geometry = None

    def get_coordinates(self, _dtype=tuple): """prototype"""
    def update(self, coordinates): """prototype"""

    #Reference to the node that is currently highlighted.
    highlight_node = None

    #List of currently selected elements.
    selected = []

    def __init__(self):
        """
        Constructor
        """
        #Pylint doesn't see self.base members...
        #pylint: disable=no-member

        assert(self.names), """
        Select.__init__(): No names defined.  Is Base inherited?
        """

        assert(self.event), """
        Select.__init__(): No event node defined.  Is Event inherited?
        """

        self.handle_select_events = True

        self.select = coin.SoType.fromName("SoFCSelection").createInstance()

        self.select.documentName.setValue(self.names[2])
        self.select.objectName.setValue(self.names[1])
        self.select.subElementName.setValue(self.names[0])

        self.select.setName(self.name + '_SELECT')
        self.base.insert_node(self.select, self.base.top)

        self.select_mouse_cb = None
        self.select_button_cb = None

        super().__init__()

    def add_select_events(self):
        """
        Add the event callbacks to the coin graph for selection
        """

        self.select_mouse_cb = self.add_mouse_event(self.select_mouse_event)
        self.select_button_cb = self.add_button_event(self.select_button_event)

    def is_selected(self):
        """
        Return whether or not the node is selected at all
        """

        return self in Select.selected

    def select_mouse_event(self, user_data, event_cb):
        """
        Mouse override
        """

        self.update_highlight()

        if self.handle_select_events or self.handle_events:
            event_cb.setHandled()

    def select_button_event(self, user_data, event_cb):
        """
        Button override
        """

        if self.mouse_state.button1.pressed:
            self.do_selection()

        #sink / consume events
        if self.handle_select_events or self.handle_events:
            event_cb.setHandled()

        self.on_select()

    def on_select(self):
        """
        Overridable callback after selection has occurred
        """

        pass

    def update_highlight(self):
        """
        Set the node currently being highlighted by the mouse
        Also clears the currently highlighted tracker
        """

        #quit if node is already highlighted
        if Select.highlight_node is self:
            return

        _no_component = self.mouse_state.component == ''

        #unhighlight the current node if it exists
        if Select.highlight_node:

            #and this is a event-consuming tracker or no component was found
            #under the mouse
            if self.handle_select_events or _no_component:

                if not Select.highlight_node.is_selected():

                    Select.highlight_node.set_style(
                        Select.highlight_node.coin_style)

                    Select.highlight_node = None

        #Don't highlight the current tracker if it's been selected
        #or no component was found under the mouse
        if self.is_selected() or _no_component:
            return

        if self.handle_select_events:
            #highlight and set current node as highlighted node
            self.set_style(CoinStyles.SELECTED)

            Select.highlight_node = self

    def do_selection(self):
        """
        Perform selection
        """

        #multi-select mode
        if self.mouse_state.ctrl_down:
            self.do_multi_select()

        #single-select cases when multiple items are selected
        elif len(Select.selected) > 1:

            if self.is_selected():
                self.do_multi_select()

            else:
                self.do_single_select()

        #single-select mode
        else:
            self.do_single_select()

    def do_single_select(self):
        """
        Manage tracker single selection
        """

        #event is consumed and a component is under the mouse
        if self.handle_select_events and self.mouse_state.component:

            self.set_style(CoinStyles.SELECTED)

            for _v in Select.selected:
                _v.set_style(_v.coin_style)

            Select.selected = [self]

            return

        #otherwise, clear all
        self.set_style(self.coin_style)

        for _v in Select.selected:
            _v.set_style(_v.coin_style)

        Select.selected = []

    def do_multi_select(self):
        """
        Manage tracker multi-selection
        """

        #requires event consumer and non-empty mouse component
        if not (self.handle_select_events and self.mouse_state.component):
            return

        _style = self.coin_style

        if self.is_selected():

            _idx = Select.selected.index(self)
            del Select.selected[_idx]

        else:

            Select.selected.append(self)
            _style = CoinStyles.SELECTED

        self.set_style(_style)

    def finish(self):
        """
        Cleanup
        """

        self.select = None
        Select.selected = []
        Select.highlight_node = None
