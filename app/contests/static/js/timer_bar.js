// Update contest time remaining bar
function loadTimerBar(contest_start, is_contest_started, is_contest_ended, contest_length, home_url) {
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

    var secondFraction = '5'; // determines progress-bar animation speed
    $('#progress-slow').css('animation', secondFraction + 's linear 0s normal none infinite progress-bar-stripes');

    var start_time = moment(contest_start, 'YYYY-MM-DD hh:mm:ss a');
    var length_time = moment(contest_length, 'HH:mm');
    var length = length_time.hour() * 3600 + length_time.minute() * 60;
    var end_time = moment(start_time).add(length_time.hour(), 'hours').add(length_time.minute(), 'minutes');
    var warning_time = moment(start_time).add(length * 0.90, 'seconds'); // 10% of contest length left
    var danger_time = moment(start_time).add(length * 0.75, 'seconds'); // 25% of contest length left
    var last_minute_time = moment(end_time).subtract(1, 'minutes');
    var viewable_time = moment(end_time).add(1, 'minutes');

    var percentage_increment = 100 / length; // the amount to increase the percentage bar per minute
    var progress_bar_percentage;

    var live_timer_div = $(".live_timer_div");
    var time_remaining_text = $(".time_remaining_text");

    var update = function () {

        function updateDuration(curr_time) {
            curr_time = moment(curr_time, 'YYYY/MM/DD HH:mm:ss');
            var time_remaining = moment.duration(end_time.diff(curr_time)).asSeconds();
            if (curr_time.isBefore(end_time)) {
                var hours_remaining = ('0' + Math.floor(time_remaining / 3600)).slice(-2);
                var minutes_remaining = ('0' + Math.floor((time_remaining % 3600) / 60)).slice(-2);
                var seconds_remaining = ('0' + (time_remaining % 60).toFixed()).slice(-2);

                time_remaining_text.html(hours_remaining + 'h : ' + minutes_remaining + 'm : ' + seconds_remaining + 's remaining');
                /*var hour_string = hours_remaining == 1 ? 'hour' : 'hours';
                 var minute_string = minutes_remaining == 1 ? 'minute' : 'minutes';
                 if(hours_remaining >= 1) {
                 time_remaining_text.html(hours_remaining + ' ' + hour_string + ' ' + minutes_remaining + ' ' + minute_string + ' remaining');
                 } else if(minutes_remaining >= 1) {
                 time_remaining_text.html(minutes_remaining + ' ' + minute_string + ' remaining');
                 } else {
                 time_remaining_text.html(seconds_remaining + ' seconds remaining');
                 }*/

                progress_bar_percentage = time_remaining * percentage_increment;
                live_timer_div.css("width", progress_bar_percentage + "%");

                if (curr_time.isAfter(warning_time)) { // 10% of contest length left
                    live_timer_div.removeClass("progress-bar-success progress-bar-warning");
                    live_timer_div.addClass("progress-bar-danger");
                } else if (curr_time.isAfter(danger_time)) { // 25% of contest length left
                    live_timer_div.removeClass("progress-bar-success progress-bar-danger");
                    live_timer_div.addClass("progress-bar-warning");
                }

                if (curr_time.isSame(last_minute_time)) {
                    window.alert("You have 1 minute remaining.");
                }
            } else {
                // contest is over, past contest may be viewed 1 minute after ending
                is_contest_ended = true;
                if (curr_time.isBefore(viewable_time)) {
                    window.alert("The contest is now over! You may view it 1 minute after it has ended.");
                    window.location.replace(home_url);
                } else {
                    // any additional 'view past contest' logic
                }
            }
        }

        updateDuration(moment());
    };

    if (is_contest_started && !is_contest_ended) { // keep refreshing contest if active contest
        update();
        setInterval(update, 1000);
    }

    if (!is_contest_started || is_contest_ended) { // disallow code submission if unstarted or past contest
        $("#id_code_file").prop('disabled', true);
        $("input[type='submit']").prop('disabled', true);
    }
}