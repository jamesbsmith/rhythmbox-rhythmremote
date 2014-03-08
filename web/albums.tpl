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
%artist = urllib.quote_plus(artist)
<ul data-role="listview" 
    data-inset="true" 
    data-filter="true" 
    data-autodividers="false">
	%for album in albums:
		%enc_album = urllib.quote_plus(album)
	    <li><a data-transition="slidefade" 
	            href="/tracks/{{artist}}/{{enc_album}}">{{album}}</a>
	         <a class="album_popup_select_link" 
	            data-rb-album="{{enc_album}}"
	            href=""
	            data-transition="pop" 
	            data-rel="popup">Select action</a></li>
	%end
</ul>
%for album in albums:
    %enc_album = urllib.quote_plus(album)
    <div data-role="popup" data-position-to="origin" 
            id="album_popup_select_{{enc_album}}" data-theme="a">
        <ul data-role="listview" data-inset="true"
                style="min-width:210px;" data-theme="b">
            <li data-role="divider" data-theme="a">Select album action</li>
            <li><a class="album_play_link" data-rb-album="{{enc_album}}"
                    href="#">Play album</a></li>
            <li><a class="album_queue_link" data-rb-album="{{enc_album}}"
                    href="#">Add album to queue</a></li>
            <li><a href="#">Add album to Playlist</a></li>
            <li><a href="#">Properties</a></li>
        </ul>
    </div>
%end
%rebase layout backlink=backlink
