$(function() {
    $('a#start-indexing-btn').bind('click', function() {
        console.log("clicked");
        $.getJSON($SCRIPT_ROOT + '/index_images', function(data) {
            console.log(data);
            $("#pokemon-in-elastic").text(data.result);
        });
        return false;
    });

    $('a#delete-index-btn').bind('click', function() {
        console.log("clicked");
        $.getJSON($SCRIPT_ROOT + '/delete_index', function(data) {
            console.log(data);
            $("#pokemon-in-elastic").text(data.result);
        });
        refresh_pokemom_in_elastic
        return false;
    });

    function refresh_pokemom_in_elastic() {
        $.getJSON($SCRIPT_ROOT + '/count_indexed_images', function(data) {
            console.log(data);
            $("#pokemon-in-elastic").text(data.count);
        });
    }
});
