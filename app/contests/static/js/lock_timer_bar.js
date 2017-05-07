// Lock time remaining bar to top of visible frame when scrolling down
$(document).ready(function() {
    if(typeof is_contest_started !== 'undefined' && is_contest_started) {
        var timer_bar = $(".progress");
        var progress_width = timer_bar.width();
        var height_above_timer = timer_bar.offset().top - parseFloat(timer_bar.css('margin-top').replace(/auto/, 0));
        var body_height = $(document).height();

        function lockTimerBarToTop() {
            var distanceFromTop = $(window).scrollTop();
            if (distanceFromTop >= height_above_timer) {
                timer_bar.fadeIn(400).addClass('fixed');
                $('html, body').css('height', body_height + 200);
            } else {
                timer_bar.fadeIn(400).removeClass('fixed');
                $('html, body').css('height', body_height);
            }
            timer_bar.width(progress_width);
        }

        $(window).scroll(lockTimerBarToTop);
    }
});
