$('#team-search-form').change(function() {
    $.ajax({
        url : $(this).attr('action'),
        type : $(this).attr('method'),
        data : $(this).serialize(),
        success : function(data, textStatus, xhr) {
            if (xhr.status == 200) {
                // Use existing tab if present
                var tab = $(data.tab);
                var href = tab.children().first('a').attr('href');
                var target = $('#team-tabs a[href="'+href+'"]');
                if (target.exists()) {
                    target.click();
                } else {
                    // Remove other search panels
                    $('#team-panels .search-panel').remove();
                    // Add tab-pane
                    var panel = $(data.panel).addClass('search-panel');
                    panel.find('input[type=checkbox][data-toggle^=toggle]').bootstrapToggle();
                    $('#team-panels').append(panel);
                    // Clear search tabs
                    $('#team-tabs .search-tab').remove();
                    // Add new tab
                    $('#team-tabs').append(tab.addClass('search-tab hidden'));
                    // Show new tab
                    $('#team-tabs li.search-tab:last a').click();
                }
            } else if (xhr.status == 201) {
                console.log('Get team failed.');
            }
        },
        error : function(data) {
            console.log('Get team failed.');
        }
    });
});