$(function() {
  var createTeamToggleButton = $("#create-team-toggle-button");
  var createTeamToggleWrapper = $("#create-team-toggle-wrapper");
  var createTeamToggleForm = $("#create-team-form");

  var joinTeamToggleButton = $("#join-team-toggle-button");
  var joinTeamToggleWrapper = $("#join-team-toggle-wrapper");
  var joinTeamToggleForm = $("#join-team-form");

  var leaveTeamToggleButton = $("#leave-team-toggle-button");
  var leaveTeamToggleWrapper = $("#leave-team-toggle-wrapper");
  var leaveTeamToggleForm = $("#leave-team-form");

  createTeamToggleButton.click(function() {
    createTeamToggleWrapper.toggleClass('open'); /* <-- toggle the application of the open class on click */
  });

  joinTeamToggleButton.click(function() {
    joinTeamToggleWrapper.toggleClass('open');
  });

  leaveTeamToggleButton.click(function() {
    leaveTeamToggleWrapper.toggleClass('open');
  });

});