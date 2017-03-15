function refreshPage() {
    var refreshSubmissionUrl = $('#refreshSubmissionUrl').html();
    var contestId = $('#contestId').html();

    $.ajax({
        url: refreshSubmissionUrl,
        data: {contestId: contestId},
        method: 'post',
        success: function (data) {
            console.log("try refresh submission")
            $('#submission_table').html(data)
        },
        complete: function () {
            setTimeout(refreshPage, 5000);
        },
    });
}

setTimeout(refreshPage, 5000);