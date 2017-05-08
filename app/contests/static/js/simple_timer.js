// Update contest time for active contests on index page
function loadTimer(time_remaining_text, contest_start, contest_length) {
    var hours = Number(contest_length.substring(0, 2));
    if (contest_length.indexOf("a.m.") != -1) {
        if (hours == 12) {
            contest_length = '00' + contest_length.substring(2);
        }
    } else {
        if (hours != 12) {
            hours += 12;
            contest_length = '' + hours + contest_length.substring(2);
        }
    }

    var start_time = moment(contest_start, 'YYYY-MM-DD hh:mm:ss a');
    var length_time = moment(contest_length, 'HH:mm');
    var end_time = moment(start_time).add(length_time.hour(), 'hours').add(length_time.minute(), 'minutes');

    var update = function () {

        function updateDuration(curr_time) {
            curr_time = moment(curr_time, 'YYYY/MM/DD HH:mm:ss');
            var time_remaining = moment.duration(end_time.diff(curr_time)).asSeconds();
            if (curr_time.isBefore(end_time)) {
                var hours_remaining = ('0' + Math.floor(time_remaining / 3600)).slice(-2);
                var minutes_remaining = ('0' + Math.floor((time_remaining % 3600) / 60)).slice(-2);
                var seconds_remaining = ('0' + (time_remaining % 60).toFixed()).slice(-2);

                time_remaining_text.html(hours_remaining + ':' + minutes_remaining + ':' + seconds_remaining + ' remaining');
            } else {
                // force page refresh to move contest out of active contests when it finishes
                window.location.reload();
            }
        }

        updateDuration(moment());
    };

    update();
    setInterval(update, 1000);
}