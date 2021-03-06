// Lock time remaining bar to top of visible frame when scrolling down
function loadLockTimerBar(is_contest_started) {
    if (typeof lock_timer_bar !== 'undefined' && !lock_timer_bar) {
        return;
    }
    if(typeof is_contest_started !== 'undefined' && is_contest_started) {
        var timer_bar = $(".progress");
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
            resizeTimerBar();
        }

        function resizeTimerBar() {
            timer_bar.width(timer_bar.parent().width());
        }

        $(window).resize(resizeTimerBar);

        $(window).scroll(lockTimerBarToTop);
    }
}
