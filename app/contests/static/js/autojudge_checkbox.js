function toggleCheckbox() {
    if ($("#id_autojudge_enabled").prop('checked') == true) {
        $("#id_autojudge_review").prop('disabled', false);
    } else {
        $("#id_autojudge_review").prop('disabled', true);
    }
}

$("#id_autojudge_enabled").click(toggleCheckbox);