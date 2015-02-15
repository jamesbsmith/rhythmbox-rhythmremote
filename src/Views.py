# -----------------------------------------------------------------------------
# - Copyright (c) 2012 Christian Ertler.
# - All rights reserved. This program and the accompanying materials
# - are made available under the terms of the GNU Public License v3.0
# - which accompanies this distribution, and is available at
# - http://www.gnu.org/licenses/gpl.html
# -
# - Contributors:
# -     Christian Ertler - initial API and implementation
# -     James B. Smith - improve browsing
# -----------------------------------------------------------------------------

import bottle
import os
import urllib
from src.WebPlayer import DBAccess, PlayerControl


class Views:

    rbplugin = None

    @staticmethod
    def add_template_path(path):
        try:
            web_path = Views.rbplugin.find_file(path)

            if web_path is None:
                web_path = os.path.abspath(path)
                print ("Cant't find web folder! Using: " + web_path)

            bottle.TEMPLATE_PATH.append(web_path)
        except NameError:
            print ("You need to assign Views.rbplugin first!")
            raise

    @staticmethod
    @bottle.route("/script/<filepath:path>")
    def static_script(filepath):
        filepath = urllib.parse.unquote_plus(filepath)
        script_path = ""
        try:
            script_path = Views.rbplugin.find_file("web/script/")

            if script_path is None:
                script_path = os.path.abspath("web/script") + "/"
                print ("Cant't find script folder! Using: " + script_path)

            return bottle.static_file(filepath, root=script_path)
        except NameError:
            print ("You need to assign Views.rbplugin first!")
            raise

    @staticmethod
    @bottle.route("/")
    @bottle.view("artists")
    def index():
        return dict(artists=order_set(DBAccess().get_all_albumartists()))

    @staticmethod
    @bottle.route("/albums/<artist:path>")
    @bottle.view("albums")
    def albums(artist):
        artist = urllib.parse.unquote_plus(artist)
        return dict(
            albums=order_set(DBAccess().get_albums_of_albumartist(artist)),
            artist=artist,
            backlink=("/", "Artists"))

    @staticmethod
    @bottle.route("/tracks/<artist:path>/<album:path>")
    @bottle.view("tracks")
    def tracks(artist, album):
        albumartist = urllib.parse.unquote_plus(artist)
        album = urllib.parse.unquote_plus(album)
        tracks = order_track_set(
            DBAccess().get_tracks_of_album(albumartist, album))
        backlink=("/albums/" + albumartist, albumartist)
        return dict(
            tracks=tracks, 
            artist=albumartist,
            album=album,
            backlink=backlink)

    @staticmethod
    @bottle.route("/playlist/<playlist:path>")
    @bottle.view("playlist")
    def playlist(playlist):
        playlist = urllib.parse.unquote_plus(playlist)
        return dict(tracks=PlayerControl().get_playlist_entries(playlist),
                    playlist=playlist,
                    backlink=("/", "Home"))

    @staticmethod
    @bottle.route("/play/<entry_id:int>")
    def play_entry(entry_id):
        player = PlayerControl()
        player.play_entry(entry_id)
        return "1"

    @staticmethod
    @bottle.route("/add_to_queue/<entry_id:int>")
    def add_to_queue(entry_id):
        PlayerControl().add_entry_to_queue(entry_id)
        return "1"

    @staticmethod
    @bottle.route("/add_album_of_entry_to_queue/<entry_id:int>")
    def view_add_album_of_entry_to_queue(entry_id):
        PlayerControl().add_album_of_entry_to_queue(entry_id)
        return "1"

    @staticmethod
    @bottle.route("/add_album_to_queue/<artist:path>/<album:path>")
    def view_add_album_to_queue(artist, album):
        artist = urllib.parse.unquote_plus(artist)
        album = urllib.parse.unquote_plus(album)
        PlayerControl().add_album_to_queue(artist, album)
        return "1"

    @staticmethod
    @bottle.route("/play_album/<artist:path>/<album:path>")
    def view_play_album(artist, album):
        artist = urllib.parse.unquote_plus(artist)
        album = urllib.parse.unquote_plus(album)
        PlayerControl().play_album(artist, album)
        return "1"

    @staticmethod
    @bottle.route("/play/<name>")
    def play(name):
        # For firefox: Use cache to answer duplicate GET requests.
        bottle.response.set_header('Cache-Control', 'max-age=1')
        PlayerControl().play(name)

    @staticmethod
    @bottle.route("/play_queue/<entry_id:int>")
    def play_queue(entry_id):
        PlayerControl().play_entry_from_queue(entry_id)

    @staticmethod
    @bottle.route("/play/<playlist>/<entry_id:int>")
    def play_playlist_entry(playlist, entry_id):
        PlayerControl().play_entry_from_playlist(entry_id, playlist)

    @staticmethod
    @bottle.route("/prev")
    def play_previous():
        # For firefox: Use cache to answer duplicate GET requests.
        bottle.response.set_header('Cache-Control', 'max-age=1')
        PlayerControl().previous()

    @staticmethod
    @bottle.route("/next")
    def play_next():
        # For firefox: Use cache to answer duplicate GET requests.
        bottle.response.set_header('Cache-Control', 'max-age=1')
        PlayerControl().next()

    @staticmethod
    @bottle.route("/pause")
    def pause():
        # For firefox: Use cache to answer duplicate GET requests.
        bottle.response.set_header('Cache-Control', 'max-age=1')
        PlayerControl().pause()

    @staticmethod
    @bottle.route("/stop")
    def stop():
        PlayerControl().stop()

    @staticmethod
    @bottle.route("/seek/<position:int>")
    def seek(position):
        PlayerControl().seek(position)

    @staticmethod
    @bottle.route("/volume")
    def get_volume():
        return str(PlayerControl().get_volume())

    @staticmethod
    @bottle.route("/volume/<volume:float>")
    def set_volume(volume):
        player = PlayerControl()
        player.set_volume(volume)
        return str(player.get_volume())

    @staticmethod
    @bottle.route("/playerinfo")
    def get_player_info():
        player = PlayerControl()
        return {"volume"       : player.get_volume(),
                "playing"      : player.is_playing(),
                "play_or_pause": player.get_playing_entry_id() >= 0,
                "has_next"     : player.has_next(),
                "has_prev"     : player.has_prev(),
                "title"        : player.get_playing_entry_str(),
                "duration"     : player.get_playing_duration(),
                "position"     : player.get_playing_time(),
                "queue_entries": player.get_queue_entries(),
                "playlists"    : player.get_playlist_names()}


def order_set(_set):
    return sorted(list(_set))


def order_track_set(_set):
    return sorted(list(_set), key=lambda x: x[1])
