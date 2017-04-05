function openInviteModal(event) {
    // Open modal
    $($(this).attr('data-target')).modal();
    event.stopPropagation();
}; $('.panel-heading a').click(openInviteModal);