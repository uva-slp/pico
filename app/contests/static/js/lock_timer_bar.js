// Lock time remaining bar to top of visible frame when scrolling down
function lockTimerBarToTop() {
    if(typeof is_contest_started !== 'undefined' && is_contest_started) {
        var distanceFromTop = $(document).scrollTop();
        var navbar_height = $("#main-navbar").height();
        var progress_width = $(".progress").width();
        if (distanceFromTop >= navbar_height) {
            $(".progress").fadeIn(400).addClass('fixed');
            $(".progress").width(progress_width);
        } else {
            $(".progress").fadeIn(400).removeClass('fixed');
            $(".progress").width(progress_width);
        }
    }
}

$(window).scroll(lockTimerBarToTop);