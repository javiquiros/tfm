$(function() {
    $('#refresh-btn').bind('click', function() {
        location.reload();
    });

    $('a#populate-db-btn').bind('click', function() {
        $.getJSON($SCRIPT_ROOT + '/populate_db', function(data) {
        });
        return false;
    });

    $('a#start-indexing-btn').bind('click', function() {
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
        refresh_pokemom_in_elastic()
        return false;
    });

    function refresh_pokemom_in_elastic() {
        $.getJSON($SCRIPT_ROOT + '/count_indexed_images', function(data) {
            $("#pokemon-in-elastic").text(data.count);
        });
    }

    $(function() {
        $('#upload-file-btn').click(function() {
            $(".spinner").show();
            $("#results").hide();
            var form_data = new FormData($('#upload-file')[0]);
            $.ajax({
                type: 'POST',
                url: '/search_image',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                success: function(data) {
                    $(".spinner").hide();
                    $("#results").show();
                    for (var i = 0; i < 4; i++) {
                        result = data[i];
                        n = i + 1
                        $("#result_name_" + n).text(result["name"]);
                        $("#result_score_" + n).text("Score: " + result["score"]);
                        image_url = "/images/" + result["id"] + ".png"
                        $("#result_image_" + n).attr("src", image_url);
                    }
                },
            });
        });
    });
});
