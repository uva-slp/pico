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

$('a[data-toggle="pill"]').on('shown.bs.tab', function(e) {
    // Re-render toggle to properly determine size
    var input = $('.tab-pane.active input[type=checkbox][data-toggle^=toggle]');
    input.bootstrapToggle('destroy');
    input.bootstrapToggle();
})
