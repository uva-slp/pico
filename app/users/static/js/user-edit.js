function userEditClick() {
    $(this).closest('div.form-group').addClass('editing');
    // Focus and move cursor to end
    var input = $(this).siblings('form').find('input.form-control');
    input.focus().val(input.val());
};
$('.btn-edit').click(userEditClick);

function cancelUserEditClick() {
    $(this).closest('div.form-group').removeClass('editing');
}
$('.btn-cancel').click(cancelUserEditClick);

function submitUserEditForm(event) {
    event.preventDefault();
    var frm = $(this);
    var frmGrp = frm.closest('div.form-group');
    var input = frm.find('input.form-control');
    $.ajax({
        url : $(this).attr('action'),
        type : $(this).attr('method'),
        data : $(this).serialize(),
        success : function(data, textStatus, xhr) {
            if (xhr.status == 200) {
                // Remove error on input
                frmGrp.removeClass('has-error');
                frmGrp.find('.help-block').text('');
                // Update input value
                if (data.val == '') {
                    frm.siblings('span.input-text').text('(none)');
                } else {
                    frm.siblings('span.input-text').text(data.val);
                }
                // Finish editing
                frmGrp.removeClass('editing');
            } else if (xhr.status == 201) {
                // Indicate error on input
                frmGrp.addClass('has-error');
                frmGrp.find('.help-block').text(data.error);
            }
        },
        error : function(data) {
            console.log('Edit user failed.');
        }
    });
}
$('.user-edit-form').on('submit', submitUserEditForm);