// Add class .active to current menu item
if (window.location.hash != '#') {
    var url = window.location.href;
    var element = $('#main-navbar ul.nav a').filter(function() {
        return $(this).attr('href') && !this.href.endsWith('#') && url.startsWith(this.href);
    }).parent();

    while (true) {
        if (element.is('li')) {
            element = element.addClass('active').parent().parent();
        } else {
            break;
        }
    }
}