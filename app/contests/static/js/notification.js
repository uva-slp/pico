function fetchNotification() {
    var getNotificationUrl = $('#getNotificationUrl').html();

    $.ajax({
        url: getNotificationUrl,
        method: 'get',
        success: function (data) {
            renderNotification(data);
        },
        complete: function () {
            setTimeout(fetchNotification, 5000);
        },
    });
}

// fetch from serve
setTimeout(fetchNotification, 5000);

// Assume we've already have a string
function renderNotification(data) {
    var l = data['data']

    if (!l) return;

    var listLenth = l.length;
    if (listLenth == 0) return;

    var modalHtml = "";
    for (var i = 0; i < listLenth; i++){
        var currentData = l[i];
        console.log("Show notification "+ currentData[4] +" for submission id " + currentData[2]);
        modalHtml += formatSingleNotification(l[i]);
    }

    $('#notificationModal').html(modalHtml);
    $('.notificationClass').modal('show');

    $('.notificationClass').on('hidden.bs.modal', function(e){
        onModalClose($(this).attr('id'));
    })
}

function onModalClose(data) {
    var stringId = data;
    console.log("stringId: " + stringId);
    var id = parseInt(stringId.substring(7));
    console.log("Try close notification: " + id);
    closeNotification(id);
}

function formatSingleNotification(data){
    var modalHtml =
        '<div class="modal fade notificationClass" id="myModal';
    modalHtml += data[4];  // append modal id
    modalHtml += '" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">'
         + '<div class="modal-dialog" role="document">'
         + '<div class="modal-content">'
         + '<div class="modal-header">'
         + '<h5 class="modal-title" id="exampleModalLabel">Status Change</h5>'
         + '<button type="button" class="close" data-dismiss="modal" aria-label="Close">'
         + '<span aria-hidden="true">&times;</span>'
         + '</button>'
         + '</div>'
         + '<div class="modal-body">';

    var notiString = "";
    notiString += "Result for Contest[ " + data[0] + " ] Problem[ "
            + data[1] + " ] Submission[ " + data[2] + " ] :";
    if (data[3] == "Yes") {
        notiString += "<b style=\"color:green;\">" + data[3] + "</b>";
    } else {
        notiString += "<b style=\"color:red;\">" + data[3] + "</b>";
    }

    modalHtml += notiString;

    modalHtml +=
        '</div>'
        + '<div class="modal-footer">'
        + '<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>'
        + '</div>'
        + '</div>'
        + '</div>'
        + '</div>';

    return modalHtml;
}

function closeNotification(data) {
    var closeNotificationUrl = $('#closeNotificationUrl').html();

    $.ajax({
        url: closeNotificationUrl,
        data: {id: data},
        method: 'post',
        success: function (data) {
        },
    });
}