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
            updataDataTable();
        },
        complete: function () {
            setTimeout(refreshPage, 5000);
        },
    });
}

setTimeout(refreshPage, 5000);

function updataDataTable() {
    $('#mydata1').DataTable({
        "searching": false,
        "lengthChange": false,
        "info": false,
        "paging": false
    });
    $('#mydata2').DataTable({
        "searching": false,
        "lengthChange": false,
        "info": false,
        "paging": false
    });
}