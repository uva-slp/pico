function fetchNotification() {


    $.ajax({
        url: "/c/api/get_notification/",
        success: function (data) {
            renderNotification(data);
            console.log(data);
        },
        complete: function () {
            setTimeout(fetchNotification, 5000);
        }
    });
}

// fetch from serve
setTimeout(fetchNotification, 5000);

// Assume we've already have a string
function renderNotification(data) {
    var l = data['data']
    var notiString = "<ul>";
    var listLenth = l.length;

    if (listLenth == 0) return;

    for (var i = 0; i < listLenth; i++){
        notiString += "<li>";
        var curData = l[i];
        notiString += "Result for Contest[ " + curData[0] + " ] Problem[ "
            + curData[1] + " ] Submission[ " + curData[2] + " ] :";
        if (curData[3] === "Yes") {
            notiString += "<b style=\"color:green;\">" + curData[3] + "</b>";
        } else {
            notiString += "<b style=\"color:red;\">" + curData[3] + "</b>";
        }


        notiString += "</li>";
    }
    notiString += "<ul>";

    $('#modalBody').html(notiString);
    $('#myModal').modal('show');
}