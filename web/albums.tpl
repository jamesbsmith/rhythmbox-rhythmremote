<!--
Copyright (c) 2012 Christian Ertler.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU Public License v3.0
which accompanies this distribution, and is available at
http://www.gnu.org/licenses/gpl.html

Contributors:
    Christian Ertler - initial API and implementation
    James B. Smith - improve browsing
-->

%import urllib
%enc_artist = urllib.quote_plus(artist)
<ul data-role="listview" 
    data-inset="true" 
    data-filter="true" 
    data-autodividers="false">
	%for album in albums:
		%enc_album = urllib.quote_plus(album[0])
	    <li><a data-transition="slidefade" 
	            href="/tracks/{{enc_artist}}/{{enc_album}}">{{album[0]}}</a>
	         <a class="album_popup_select_link" 
	            data-rb-album="{{enc_album}}"
	            data-rb-album-id="{{album[1]}}"
	            href=""
	            data-transition="pop" 
	            data-rel="popup">Album Action</a></li>
	%end
</ul>
%for album in albums:
    %enc_album = urllib.quote_plus(album[0])
    <div data-role="popup" 
            data-position-to="origin" 
            id="album_popup_select_{{album[1]}}" data-theme="a">
        <ul data-role="listview" 
                data-inset="true"
                style="min-width:210px;" 
                data-theme="b">
            <li data-role="divider" 
                    data-theme="a">Select Album Action</li>
            <li><a class="album_play_link" 
                    data-rb-enc-album="{{enc_album}}"
                    data-rb-album="{{album[0]}}" 
                    data-rb-album-id="{{album[1]}}"
                    data-rb-albumartist="{{artist}}" 
                    data-rb-enc-artist="{{enc_artist}}"
                    href="#">Play album</a></li>
            <li><a class="album_queue_link" 
                    data-rb-enc-album="{{enc_album}}"
                    data-rb-album="{{album[0]}}" 
                    data-rb-album-id="{{album[1]}}"
                    data-rb-albumartist="{{artist}}" 
                    data-rb-enc-artist="{{enc_artist}}"
                    href="#">Add album to queue</a></li>
            <li><a href="#">Add album to Playlist</a></li>
            <li><a href="#">Properties</a></li>
        </ul>
    </div>
%end
%rebase layout backlink=backlink
