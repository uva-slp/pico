function UpdatePanelHeaders() {
  $(".panel.fixed-header").each(function() {
    var el         = $(this),
    offset         = el.offset(),
    scrollTop      = $(window).scrollTop(),
    floatingHeader = $(".floatingHeader", this),
	absoluteHeader = $(".absoluteHeader", this);

    if ((scrollTop > offset.top) && (scrollTop < offset.top + (el.height() - floatingHeader.outerHeight(false)) + 4)) {
      floatingHeader.css({
        "visibility": "visible"
      });
      absoluteHeader.css({
        "visibility": "hidden"
      });
	} else if (scrollTop  > (offset.top + el.height() - floatingHeader.outerHeight(false))) {
      absoluteHeader.css({
        "visibility": "visible",
		"top": (el.height() + offset.top - floatingHeader.outerHeight(true) + 4 )
      });
      floatingHeader.css({
        "visibility": "hidden"
      });
    } else {
      floatingHeader.css({
        "visibility": "hidden"
      });
      absoluteHeader.css({
        "visibility": "hidden"
      });
    }
  });
}

function loadPanelCopies() {
  var clonedHeaderRow;
  var secondClonedHeaderRow;
  
  $(".panel.fixed-header").each(function() {
    clonedHeaderRow = $(".panel-heading", this);
    clonedHeaderRow
    .before(clonedHeaderRow.clone())
    .css("width", clonedHeaderRow.outerWidth())
    .addClass("floatingHeader");
	
	secondClonedHeaderRow = $(".floatingHeader", this);
    secondClonedHeaderRow
    .before(secondClonedHeaderRow.clone())
    .css("width", secondClonedHeaderRow.outerWidth())
	.removeClass("floatingHeader")
    .addClass("absoluteHeader");
  });
}

function reloadPanelCopies() {
  $(".floatingHeader").remove();
  $(".absoluteHeader").remove();
  loadPanelCopies();
}

var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();

// DOM Ready
$(function() {
  
  loadPanelCopies();
  
  $(window).resize(function() {
    delay(function(){
      reloadPanelCopies();
    }, 100);
  });
  
  $(window)
  .scroll(UpdatePanelHeaders)
  .trigger("scroll");
   
});