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
    $('#modalBody').html(JSON.stringify(data));
    $('#myModal').modal('show');
}