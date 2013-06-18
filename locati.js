var LOCATIAPP = "http://localhost:8080"

function updateResult(response) {
    var result = response.result || [];
    var origCount = response.origCount || 0;
    var count = response.count || 0;
    
    $('#result li').remove();

    $('#resultCount').html('Suchergebnisse: '+ count +' von '+ origCount);

    for (var i = 0; i < result.length; i++) {
        $('#result').append(
            $('<li>').html(result[i])
        );
    }
}

/*=====================\
 | search              |
 ================================================================*/
function onSearchChange(event){
    var phrase = $(event.target).val();
    //if (phrase.length > 2) {
        $.getJSON(LOCATIAPP+'/locate/'+phrase+'?callback=?', updateResult);
    //}
}
/*_______________________________________________________________*/

function onUpdatedbClick(event){
    $(event.target).attr("value","updating...");
    $.getJSON(LOCATIAPP+'/updatedb/?callback=?', function(response){
        return function(response) {
            $(event.target).attr("value","Update locate db");
        }
    }());
}

$('#phrase').keyup(onSearchChange);
$('#updatedb').click(onUpdatedbClick);
