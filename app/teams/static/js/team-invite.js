$('.panel-heading a').click(function( event ) {
    // Open modal
    $($(this).attr('data-target')).modal();
    event.stopPropagation();
});