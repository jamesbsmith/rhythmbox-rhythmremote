# ----------------------------------------------------------------------
# - Copyright (c) 2012 Christian Ertler.
# - All rights reserved. This program and the accompanying materials
# - are made available under the terms of the GNU Public License v3.0
# - which accompanies this distribution, and is available at
# - http://www.gnu.org/licenses/gpl.html
# -
# - Contributors:
# -     Christian Ertler - initial API and implementation
# -     James B. Smith - add schema file and preferences dialog
# ----------------------------------------------------------------------

import rb
from gi.repository import GObject, Peas, PeasGtk, Gtk, Gio
import os

# import WebPlayer, Views
# from WebServer import WSGIRefWebServer as WebServer
from src import WebPlayer, Views
from src.WebServer import WSGIRefWebServer as WebServer
from gsettings import settings


class RhythmRemotePlugin(GObject.Object, Peas.Activatable):
    __gtype_name__ = 'RhythmRemotePlugin'
    object = GObject.Property(type=GObject.GObject)

    def __init__(self):
        super(RhythmRemotePlugin, self).__init__()

    def do_activate(self):
        WebPlayer.DBAccess.rbshell = self.object
        WebPlayer.PlayerControl.rbshell = self.object
        Views.Views.rbplugin = self
        Views.Views.add_template_path("web/")

        # Get port and adress settings from schema
        port = settings.get_int("server-port")
        address = settings.get_string("server-address")
        print "starting server " + address + ":" + str(port) + " ..."
        self.__server = WebServer(address, port, "webplayer.settings")
        self.__server.start()

    def do_deactivate(self):
        print "stopping server..."
        self.__server.stop()

    def find_file(self, filename):
        info = self.plugin_info
        data_dir = info.get_data_dir()
        data_dir = data_dir.replace("/src", "/rhythmremote/")
        path = os.path.join(data_dir, filename)

        if os.path.exists(path):
            return path

        return None


class RhythmRemoteConfigurable(GObject.Object, PeasGtk.Configurable):
    __gtype_name__ = 'RhythmRemoteConfigurable'

    def __init__(self):
        GObject.Object.__init__(self)

    def do_create_configure_widget(self):
        builder = Gtk.Builder()
        builder.add_from_file(
            rb.find_plugin_file(self, "ui/rhythmremote-prefs.ui"))

        # Get the preferences dialog widgets
        self.address_entry = builder.get_object("server_ip")
        self.port_entry = builder.get_object("server_port")
        self.apply_button = builder.get_object("apply_button")
        self.prefs_frame = builder.get_object("prefs_frame")

        # Populate the Entry widgets with values stored in the schema
        self.address_entry.set_text(settings.get_string("server-address"))
        self.port_entry.set_text(str(settings.get_int("server-port")))

        # Connect a handler to update settings in the schema
        self.apply_button.connect("clicked", self.on_apply_button_clicked)

        return self.prefs_frame

    def on_apply_button_clicked(self, widget):
        # Get new values from the preferences dialog Entry widgets
        self.address = self.address_entry.get_text()
        self.port = int(self.port_entry.get_text())

        # Store the new values in the schema
        settings.set_string("server-address", self.address)
        settings.set_int("server-port", self.port)
