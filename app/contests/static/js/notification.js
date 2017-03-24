function fetchNotification() {
    var getNotificationUrl = $('#getNotificationUrl').html();

    $.ajax({
        url: getNotificationUrl,
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

    var listLenth = l.length;
    if (listLenth == 0) return;

    for (var i = 0; i < listLenth; i++){
        var currentData = l[i];
        if (($("#myModal" + currentData[4]).data('bs.modal') || {}).isShown == true) {
            console.log("notification for submission id " + currentData[5] + " is open, current modal id: " + currentData[4]);
        } else {
            console.log("notification for submission id " + currentData[5] + " is not shown, " +
                "show new modal " + currentData[4]);
            formatSingleNotification(l[i]);
        }
    }

    $('.notificationClass').modal('show');

    $('.notificationClass').on('hidden.bs.modal', function (e) {
        var stringId = $(this).attr('id');
        var id = parseInt(stringId.slice(-1));
        console.log("Try close notification: " + id);
        closeNotification(id);
    })
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
        + '</div>'
        + '</div>'
        + '</div>'
        + '</div>';

    $('#notificationModal').append(modalHtml);
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