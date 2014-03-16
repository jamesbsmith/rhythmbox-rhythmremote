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

<ul data-role="listview" data-inset="true" 
        data-filter="true" data-autodividers="false">
	%for track in tracks:
	<li><a class="track_popup_select_link" 
	    data-rb-entry-id="{{track[0]}}" 
	    href="" 
	    data-transition="pop" 
	    data-rel="popup">{{track[1]}} {{track[2]}}</a></li>
	%end
</ul>
%for track in tracks:
<div data-role="popup" data-position-to="origin" 
        id="popup_select_{{track[0]}}" data-theme="a">
	<ul data-role="listview" data-inset="true" 
	        style="min-width:210px;" data-theme="b">
		<li data-role="divider" data-theme="a">Select action</li>
		<li><a class="track_play_link" 
		    data-rb-entry-id="{{track[0]}}" 
		    data-rb-entry-name="{{track[2]}}" 
		    href="#">Play track</a></li>
		<li><a class="track_queue_link" 
		    data-rb-entry-id="{{track[0]}}" 
		    data-rb-entry-name="{{track[2]}}" 
		    href="#">Add track to Queue</a></li>
		<li><a class="track_album_play_link" 
		    data-rb-entry-id="{{track[0]}}" 
		    data-rb-entry-name="{{track[2]}}" 
		    href="#">Play album</a></li>
		<li><a class="track_album_queue_link" 
		    data-rb-entry-id="{{track[0]}}" 
		    data-rb-entry-name="{{track[2]}}" 
		    href="#">Add album to queue</a></li>
		<li><a href="#">Add to Playlist</a></li>
		<li><a href="#">Properties</a></li>
	</ul>
</div>
%end
%rebase layout backlink=backlink
