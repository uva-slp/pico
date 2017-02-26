$(document).on('change', '.team-public-form', function() {
    var frm = $(this);
    $.ajax({
        url : $(this).attr('action'),
        type : $(this).attr('method'),
        data : $(this).serialize(),
        success : function(data, textStatus, xhr) {
            console.log('Toggle team.public successful.');
        },
        error : function(data) {
            console.log('Toggle team.public failed.');
        }
    });
});