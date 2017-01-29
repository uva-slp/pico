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

    var listLenth = l.length;
    if (listLenth == 0) return;

    for (var i = 0; i < listLenth; i++){
        formatSingleNotification(l[i]);
    }

    $('.notificationClass').modal('show');
}

function formatSingleNotification(data){
    var modalHtml =
        '<div class="modal fade notificationClass" id="myModal';
    modalHtml += data[4];  // append modal id
    modalHtml += '" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">'
         + '<div class="modal-dialog" role="document">'
         + '<div class="modal-content">'
         + '<div class="modal-header">'
         + '<h5 class="modal-title" id="exampleModalLabel">Modal title</h5>'
         + '<button type="button" class="close" data-dismiss="modal" aria-label="Close">'
         + '<span aria-hidden="true">&times;</span>'
         + '</button>'
         + '</div>'
         + '<div class="modal-body">';

    var notiString = "";
    notiString += "Result for Contest[ " + data[0] + " ] Problem[ "
            + data[1] + " ] Submission[ " + data[2] + " ] :";
    if (data[3] === "Yes") {
        notiString += "<b style=\"color:green;\">" + data[3] + "</b>";
    } else {
        notiString += "<b style=\"color:red;\">" + data[3] + "</b>";
    }

    modalHtml += notiString;

    modalHtml +=
        '</div>'
        + '<div class="modal-footer">'
        + '<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>'
        + '<button type="button" class="btn btn-primary">Save changes</button>'
        + '</div>'
        + '</div>'
        + '</div>'
        + '</div>';

    $('#notificationModal').append(modalHtml);
}