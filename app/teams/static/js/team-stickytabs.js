function onClickTeamTab(event) {
    var baseURL = window.location.href;
    baseURL = baseURL.substr(0, baseURL.indexOf('/teams/')+7);
    history.replaceState('data', '', baseURL + this.href.split('#team-')[1] + '/');
}; $(document).on('click', '#team-tabs a', onClickTeamTab);