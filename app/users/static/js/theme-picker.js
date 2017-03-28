function loadThemes() {
    $.getJSON('https://bootswatch.com/api/3.json', function (data) {
        var themes = data.themes;
        var picker = $('#picker');
      
        themes.forEach(function(theme, index){
            picker.append($('<div />')
                .addClass('col-lg-4 col-sm-6')
                .append($('<div />')
                    .addClass('preview')
                    .append($('<div />')
                        .addClass('image')
                        .append($('<a />')
                            .attr('href', theme.preview)
                            .append($('<img />')
                                .addClass('img-responsive')
                                .attr('alt', theme.name)
                                .attr('src', theme.thumbnail))))
                    .append($('<div />')
                        .addClass('options')
                        .append($('<h3 />')
                            .text(theme.name))
                        .append($('<p />')
                            .text(theme.description))
                        .append($('<div />')
                            .addClass('btn-group')
                            .append($('<button />')
                                .addClass('btn btn-info')
                                .attr('type', 'submit')
                                .text('Apply Theme')
                                .click(function() {
                                    $('input#theme').val(theme.cssMin);
                                }))))))
        });

        $('#acknowledgement').removeClass('hidden');

    }, 'json').fail(function(){
        $('.alert').removeClass('hidden').addClass('alert-info alert-danger');
        $('.alert h4').text('Failed to load themes.');
    });
}; loadThemes();

$('#default-theme-btn').click(function() {
    $('input#theme').val('');
})

$('#change-theme-form').on('submit', function(event) {
    event.preventDefault();
    var frm = $(this);
    $.ajax({
        url : $(this).attr('action'),
        type : $(this).attr('method'),
        data : $(this).serialize(),
        success : function(data, textStatus, xhr) {
            if (xhr.status == 200) {
                $('.alert').addClass('hidden');
                $('link#bootstrap-css').attr('href', data.theme);
            } else if (xhr.status == 201) {
                $('.alert').removeClass('hidden').addClass('alert-info alert-danger');
                $('.alert h4').text(data.error);
            }
        },
        error : function(data) {
            console.log('Edit user failed.');
        }
    });
});