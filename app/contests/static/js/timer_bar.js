<!-- Update contest time remaining bar -->
var secondFraction = '5'; // determines progress-bar animation speed
$('#progress-slow').css('animation', secondFraction + 's linear 0s normal none infinite progress-bar-stripes');

var start_time = contest_start;
var length_time = moment(contest_length, 'hh:mm');
var length = length_time.hour() * 60 + length_time.minute();

var percentage_increment = 100 / length; // the amount to increase the percentage bar per minute
var progress_bar_percentage;

var live_timer_div = $(".live_timer_div");
var time_remaining_text = $(".time_remaining_text");

var update = function() {

    function updateDuration(start_time, curr_time) {
      var ms = moment(curr_time, 'YYYY/MM/DD HH:mm:ss').diff(moment(start_time, 'MMM DD, YYYY, hh:mm:ss a'));
      var dt = moment.duration(ms);
      var hours_elapsed = Math.floor(dt.asHours());
      var minutes_elapsed = moment.utc(ms).format('mm');
      var seconds_elapsed = moment.utc(ms).format('ss');
      var time_left = length - ((hours_elapsed * 60) + Number(minutes_elapsed) + (Number(seconds_elapsed) / 60));
      if(time_left >= 0) {
          var hours_left = ('0' + Math.floor(time_left / 60)).slice(-2);
          var minutes_left = ('0' + Math.floor(time_left % 60)).slice(-2);
          var seconds_left = ('0' + (((time_left % 60) - minutes_left) * 60).toFixed()).slice(-2);

          time_remaining_text.html(hours_left + 'h : ' + minutes_left + 'm : ' + seconds_left + 's remaining');
          /*var hour_string = hours_left == 1 ? 'hour' : 'hours';
          var minute_string = minutes_left == 1 ? 'minute' : 'minutes';
          if(hours_left >= 1) {
              time_remaining_text.html(hours_left + ' ' + hour_string + ' ' + minutes_left + ' ' + minute_string + ' remaining');
          } else if(minutes_left >= 1) {
              time_remaining_text.html(minutes_left + ' ' + minute_string + ' remaining');
          } else {
              time_remaining_text.html(seconds_left + ' seconds remaining');
          }*/

          progress_bar_percentage = time_left * percentage_increment;
          live_timer_div.css("width", progress_bar_percentage + "%");

          if (time_left <= 30) {
            live_timer_div.removeClass("progress-bar-success progress-bar-warning");
            live_timer_div.addClass("progress-bar-danger");
          } else if (time_left <= 60) {
            live_timer_div.removeClass("progress-bar-success progress-bar-danger");
            live_timer_div.addClass("progress-bar-warning");
          }
      } else {
          // contest is over, past contest may be viewed 1 minute after ending
          is_contest_ended = true;
          if(time_left >= -1) {
              window.alert("The contest is now over! You may view this contest 1 minute after it has ended.");
              window.location.replace(home_url);
          } else {
              // view past contest logic
          }
      }
    }

    updateDuration(start_time, moment().format('YYYY/MM/DD HH:mm:ss'));
};

$(document).ready(function() {
  if(is_contest_started && !is_contest_ended) {
      update();
      setInterval(update, 1000);
  }

  if(!is_contest_started || is_contest_ended) {
      $("#id_code_file").prop('disabled', true);
      $("input[type='submit']").prop('disabled', true);
      $("#timer_bar").hide();
  }
});