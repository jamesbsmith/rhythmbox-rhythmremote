# ----------------------------------------------------------------------------
# - Copyright (c) 2012 Christian Ertler.
# - All rights reserved. This program and the accompanying materials
# - are made available under the terms of the GNU Public License v3.0
# - which accompanies this distribution, and is available at
# - http://www.gnu.org/licenses/gpl.html
# -
# - Contributors:
# -     Christian Ertler - initial API and implementation
# -     James B. Smith - improve browsing:
# -         - Remove auto-dividers.
# -         - Use album-artists sorted by sortname.
# -         - Add disc-track numbers, sort by them in album/tracks view.
# -         - Use album_artist_folded as lookup key (fixes AC/DC issue).
# -         - Add 'Add album to Queue' and 'Play album' functions.            
# ----------------------------------------------------------------------------

from gi.repository import RB, GLib


# 'object' is a new-style class, the base class for all built-in
# types. Defining a new class as a sub class of 'object' is the
# easiest way to define a new class as a new-style class in 
# python 2.x. New-style classes are needed for the 'super()' function. 
class DBAccess(object):

    # rbsell is assigned when plugin is activated, in the
    # plugin class's do_activate() function.
    rbshell = None

    def __init__(self):
        try:
            self.library = DBAccess.rbshell.props.library_source
            self.db = DBAccess.rbshell.props.db
        except NameError:
            print "You need to assign DBAccess.rbshell first!"
            raise

    def get_all_albumartists(self):
        entries = set()
        type_artist_sortname = RB.RhythmDBPropType.ALBUM_ARTIST_SORTNAME
        type_artist = RB.RhythmDBPropType.ALBUM_ARTIST
        type_artist_folded = RB.RhythmDBPropType.ALBUM_ARTIST_FOLDED
        for row in self.library.props.base_query_model:
            entry = row[0]
            entries.add((
                entry.get_string(type_artist_sortname),
                entry.get_string(type_artist),
                entry.get_string(type_artist_folded)))
        return entries

    def get_all_genres(self):
        return self.__get_all_of_type(entry_type=RB.RhythmDBPropType.GENRE)

    def get_albums_of_albumartist(self, artist):
        query_model = self.__do_single_query(
            RB.RhythmDBPropType.ALBUM_ARTIST_FOLDED, artist)
        album_list = set()
        for row in query_model:
            album_list.add(row[0].get_string(RB.RhythmDBPropType.ALBUM))
        albums = set()
        album_id = 0
        # Create album_id to use in html id attributes
        for album in album_list:
            album_id = album_id + 1
            albums.add((album, album_id))
        return albums

    def get_tracks_of_album(self, albumartist, album):
        query_model = self.__do_query([
            (RB.RhythmDBPropType.ALBUM_ARTIST_FOLDED, albumartist,
                RB.RhythmDBQueryType.EQUALS),
            (RB.RhythmDBPropType.ALBUM, album,
                RB.RhythmDBQueryType.EQUALS)
        ])

        max_disc_number = 0
        for row in query_model:
            disc_number = row[0].get_ulong(RB.RhythmDBPropType.DISC_NUMBER)
            if disc_number > max_disc_number:
                max_disc_number = row[0].get_ulong(
                    RB.RhythmDBPropType.DISC_NUMBER)

        if max_disc_number > 1:
            return [
                (
                    row[0].get_ulong(RB.RhythmDBPropType.ENTRY_ID),
                    '{:d}.{:02d}'.format(
                        row[0].get_ulong(RB.RhythmDBPropType.DISC_NUMBER),
                        row[0].get_ulong(RB.RhythmDBPropType.TRACK_NUMBER)),
                    row[0].get_string(RB.RhythmDBPropType.TITLE)
                    )
                for row in query_model]
        else:
            return [
                (
                    row[0].get_ulong(RB.RhythmDBPropType.ENTRY_ID),
                    '{:02d}'.format(
                        row[0].get_ulong(RB.RhythmDBPropType.TRACK_NUMBER)),
                    row[0].get_string(RB.RhythmDBPropType.TITLE)
                    )
                for row in query_model]

    def get_entry(self, entry_id):
        return self.db.entry_lookup_by_id(entry_id)

    def __do_single_query(
            self, prop, value, query_type=RB.RhythmDBQueryType.EQUALS):
        query_model = RB.RhythmDBQueryModel.new_empty(self.db)
        query = GLib.PtrArray()

        self.db.query_append_params(query, query_type, prop, value)
        self.db.do_full_query_parsed(query_model, query)

        return query_model

    def __do_query(self, params):
        query_model = RB.RhythmDBQueryModel.new_empty(self.db)
        query = GLib.PtrArray()

        for param in params:
            self.db.query_append_params(query, param[2], param[0], param[1])
        self.db.do_full_query_parsed(query_model, query)

        return query_model

    def __get_all_of_type(self, entry_type):
        entries = set()
        for row in self.library.props.base_query_model:
            entry = row[0]
            entries.add(entry.get_string(entry_type))
        return entries


class PlayerControl(object):

    rbshell = None

    def __init__(self):
        try:
            self.__player = PlayerControl.rbshell.props.shell_player
            self.__queue = PlayerControl.rbshell.props.queue_source
            self.__library = PlayerControl.rbshell.props.library_source
            self.__dbaccess = DBAccess()
            self.__playlistManager = (
                PlayerControl.rbshell.props.playlist_manager)
        except NameError:
            print "You need to assign PlayerControl.rbshell first!"
            raise

    def __loadPlaylists(self):
        self.__playlists = dict()
        for playlist in self.__playlistManager.get_playlists():
            self.__playlists[playlist.props.name] = playlist

    def __play_entry(self, entry_id, source):
        self.__player.set_playing_source(source)
        self.__player.play_entry(self.__dbaccess.get_entry(entry_id), source)

    def __get_source_entries(self, source):
        entries = list()
        for row in source.get_query_model():
            entry = row[0]
            entry_id = entry.get_ulong(RB.RhythmDBPropType.ENTRY_ID)
            title = (
                entry.get_string(RB.RhythmDBPropType.ARTIST)
                + " - "
                + entry.get_string(RB.RhythmDBPropType.TITLE))
            entries.append((entry_id, title))
        return entries


    def play(self, unused):
        self.__player.playpause(unused)

    def play_entry(self, entry_id):
        self.__play_entry(entry_id, self.__library)

    def play_entry_from_queue(self, entry_id):
        self.__play_entry(entry_id, self.__queue)

    def play_entry_from_playlist(self, entry_id, playlist):
        self.__loadPlaylists()
        # if (self.__playlists.has_key(playlist)):
        if (playlist in self.__playlists):
            self.__play_entry(entry_id, self.__playlists[playlist])

    def add_entry_to_queue(self, entry_id):
        self.__queue.add_entry(self.__dbaccess.get_entry(entry_id), -1)

    def add_album_of_entry_to_queue(self, entry_id):
        entry = self.__dbaccess.get_entry(entry_id)
        albumartist = entry.get_string(RB.RhythmDBPropType.ALBUM_ARTIST_FOLDED)
        album = entry.get_string(RB.RhythmDBPropType.ALBUM)
        tracks = self.order_track_set(
            self.__dbaccess.get_tracks_of_album(albumartist, album))
        for track in tracks:
            self.__queue.add_entry(self.__dbaccess.get_entry(track[0]), -1)

    def add_album_to_queue(self, albumartist, album):
        tracks = self.order_track_set(
            self.__dbaccess.get_tracks_of_album(albumartist, album))
        for track in tracks:
            self.__queue.add_entry(self.__dbaccess.get_entry(track[0]), -1)

    def play_album(self, albumartist, album):
        print ("albumartist, album is: ", albumartist, album)
        # self.__loadPlaylists()
        # if ("playingAlbum" in self.__playlists):
        #     self.__playlistManager.delete_playlist("playingAlbum")
        # playlist = self.__playlistManager.new_playlist("playingAlbum", False)
        try:
            self.__playlistManager.delete_playlist("Album")
        except:
            pass
        playlist = self.__playlistManager.new_playlist("Album", False)
        tracks = self.order_track_set(
            self.__dbaccess.get_tracks_of_album(albumartist, album))
        for track in tracks:
            uri = self.__dbaccess.get_entry(track[0]).get_playback_uri()
            self.__playlistManager.add_to_playlist("Album", uri)
        self.__player.set_playing_source(playlist)
        self.__player.playpause("unused")

    def stop(self):
        self.__player.stop()

    def pause(self):
        self.__player.pause()

    def has_next(self):
        return self.__player.props.has_next

    def has_prev(self):
        return self.__player.props.has_prev

    def next(self):
        try:
            self.__player.do_next()
        except:
            pass

    def previous(self):
        try:
            self.__player.do_previous()
        except:
            pass

    def seek(self, position):
        if self.has_prev():
            self.__player.seek(position)

    def is_playing(self):
        return self.__player.get_playing()[1]

    def get_playing_entry_id(self):
        entry = self.__player.get_playing_entry()
        if (entry is None):
            return -1
        return self.__player.get_playing_entry().get_ulong(
            RB.RhythmDBPropType.ENTRY_ID)

    def get_playing_entry_str(self):
        entry = self.__player.get_playing_entry()

        if (entry is None):
            return "-"

        title = entry.get_string(RB.RhythmDBPropType.TITLE)
        artist = entry.get_string(RB.RhythmDBPropType.ARTIST)
        return "[" + artist + "] - " + title

    def get_playing_duration(self):
        if (not self.is_playing()):
            return 0
        return self.__player.get_playing_song_duration()

    def get_playing_time(self):
        print self.is_playing()
        if (not self.is_playing()):
            return 0
        return self.__player.get_playing_time()[1]

    def get_volume(self):
        return self.__player.get_volume()[1]

    def set_volume(self, volume):
        self.__player.set_volume(volume)

    def get_queue_entries(self):
        return self.__get_source_entries(self.__queue)

    def get_playlist_names(self):
        self.__loadPlaylists()
        return sorted(self.__playlists.keys())

    def get_playlist_entries(self, playlist):
        self.__loadPlaylists()
        # if (not self.__playlists.has_key(playlist)):
        if (playlist not in self.__playlists):
            return None
        else:
            return self.__get_source_entries(self.__playlists[playlist])

    def order_track_set(self, _set):
        return sorted(list(_set), cmp=lambda x,y: cmp(x[1], y[1]))
