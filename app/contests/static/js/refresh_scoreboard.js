function refreshPage() {
    var refreshScoreboardUrl = $('#refreshScoreboardUrl').html();
    var contestId = $('#contestId').html();

    $.ajax({
        url: refreshScoreboardUrl,
        data: {contestId: contestId},
        method: 'post',
        success: function (data) {
            console.log("try refresh scoreboard")
            $('#scoreboard_div').html(data)
        },
        complete: function () {
            setTimeout(refreshPage, 5000);
        },
    });
}

setTimeout(refreshPage, 5000);