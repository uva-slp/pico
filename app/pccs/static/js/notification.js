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
        notiString += l[i];
        notiString += "</li>";
    }
    notiString += "<ul>";

    $('#modalBody').html(notiString);
    $('#myModal').modal('show');
}