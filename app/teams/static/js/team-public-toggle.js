function submitTeamPublicForm(event) {
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
}; $(document).on('change', '.team-public-form', submitTeamPublicForm);

function renderToggle(event) {
    // Re-render toggle to properly determine size
    var input = $('.tab-pane.active input[type=checkbox][data-toggle^=toggle]');
    input.bootstrapToggle('destroy');
    input.bootstrapToggle();
}; $('a[data-toggle="pill"]').on('shown.bs.tab', renderToggle);
