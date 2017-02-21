$(document).on('click', '#team-tabs a', function(event) {
    history.replaceState('data', '', '{% url "teams:index" %}' + this.href.split('#team-')[1] + '/');
});