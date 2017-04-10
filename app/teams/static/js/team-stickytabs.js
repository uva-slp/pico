function onClickTeamTab(event) {
    var baseURL = window.location.href;
    baseURL = baseURL.substr(0, baseURL.indexOf('/teams/')+7);
    try { history.replaceState('data', '', baseURL + this.href.split('#team-')[1] + '/'); }
    catch (exception) { console.log(exception); }
}; $(document).on('click', '#team-tabs a', onClickTeamTab);