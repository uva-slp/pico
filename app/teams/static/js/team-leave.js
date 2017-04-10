function submitTeamLeaveForm(event) {
    event.preventDefault();
    var frm = $(this);
    $.ajax({
        url : $(this).attr('action'),
        type : $(this).attr('method'),
        data : $(this).serialize(),
        success : function(data, textStatus, xhr) {
            var team_id = frm.children('input#id_team').val();
            // Show first tab that is not the one being deleted or no teams if there are not any anymore
            var next = $('#team-tabs').find('a[href!="#"][href!="#no-teams"][href!="#team-'+team_id+'"]').first();
            next.click();
            if (!next.exists()) {
                $('#side-menu').find('a[href="#no-teams"]').click();
            }
            // Destory tab
            $('#team-tabs').find('a[href="#team-'+team_id+'"]').parent().remove();
            // Destroy tab panel
            $('#team-'+team_id).remove();
            // Change URL to index
            var baseURL = window.location.href;
            baseURL = baseURL.substr(0, baseURL.indexOf('/teams/')+7);
            try { history.replaceState('data', '', baseURL); }
            catch (exception) { console.log(exception); }
        },
        error : function(data) {
            console.log('Leave team failed.');
        }
    });
}; $(document).on('submit', '.team-leave-form', submitTeamLeaveForm);