function focusInput() {
    $(this).find('input:text:visible:first').focus();
}; $('#create-team.modal').on('shown.bs.modal', focusInput);

// Backup clean form
var team_form_clean = $('#team-form-contents').html();

function submitTeamForm(event) {
    event.preventDefault();
    $.ajax({
        url : $(this).attr('action'),
        type : $(this).attr('method'),
        data : $(this).serialize(),
        success : function(data, textStatus, xhr) {
            if (xhr.status == 200) {
                // Clear form
                $('#team-form-contents').html(team_form_clean);
                // Add item to sidemenu and re-sticky
                $('#team-tabs').append(data.tab);
                // Add tab-pane
                var panel = $(data.panel);
                $('#team-panels').append(panel);
                // Show tab that was added
                $('#team-tabs a').last().click();
                // Render data-toggle
                panel.find('input[type=checkbox][data-toggle^=toggle]').bootstrapToggle();
                // Close modal
                $('#create-team.modal').modal('hide');
            } else if (xhr.status == 201) {
                // Update form and focus on input
                $('#team-form-contents').html(data.form).find('input:text:visible:first').focus();
            }
        },
        error : function(data) {
            console.log('Create team failed.');
        }
    });
}; $('#team-form').on('submit', submitTeamForm);