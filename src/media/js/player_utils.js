    var player = null;
    tracklist = [];
    current = 0;
    currentState = 'NULL';
    previousState = 'NULL';


    function createPlayer(thePlaceholder, thePlayerId, theFile, theAutostart) {
        var flashvars = {
                file:theFile,
                autostart:theAutostart
        };
        var params = {
                allowfullscreen:"true",
                allowscriptaccess:"always"
        };
        var attributes = {
                id:thePlayerId,
                name:thePlayerId
        };
        swfobject.embedSWF(STATIC_URL + "swf/player.swf", thePlaceholder, "320", "22", "9.0.115", false, flashvars, params, attributes);
    }

    function playerReady(thePlayer) {
        player = document.getElementById(thePlayer.id);
        addListeners();
    }

    function addListeners() {
        if (player) {
            player.addModelListener("STATE", "stateListener");
        } else {
            setTimeout("addListeners()",100);
        }
    }

    function getNextTrack(current){
        for(var i=0;i<tracklist.length;i++){
            if( tracklist[i] == current ){
                if( i < tracklist.length-1 ){
                    return tracklist[i+1];
                }
            }
        }
        return tracklist[0];
    }

    function stateListener(obj) { //IDLE, BUFFERING, PLAYING, PAUSED, COMPLETED
        currentState = obj.newstate;
        previousState = obj.oldstate;

        if ((currentState == "COMPLETED")&&(previousState == "PLAYING")) {
            next = getNextTrack(current);
            closePlayer(current);
            openPlayer(next);
        }
    }

    function openPlayer(track_id){
        if( current ){
            closePlayer(current);
        }

        play_link = $('#play'+track_id);
        url = play_link.metadata().prefix + play_link.metadata().filename;
        play_link.hide();
        $('#stop'+track_id).show();
        createPlayer("player_place"+track_id, "player"+track_id, url, true);
        current = track_id;
    }

    function closePlayer(track_id){
        $('#song' + track_id).html('<div id="player_place' + track_id + '"></div>');
        $("#play" + track_id).show();
        $("#stop" + track_id).hide();
    }

    $(function(){
        $(".b-track-list .play").click( function(){
            track_id = $(this).metadata().song;
            openPlayer(track_id);
            return false;
        });

        $(".b-track-list .stop").click( function(){
            track_id = $(this).metadata().song;
            closePlayer(track_id);
            return false;
        });

        $('.play').each( function(){
            tracklist.push($(this).metadata().song);
        });
    });


