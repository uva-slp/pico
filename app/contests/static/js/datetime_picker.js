$(document).ready(function() {
            $(function () {
                $('#id_contest_length_pickers:has(input:not([readonly],[disabled]))').datetimepicker({"format": "HH:mm"});
            });
            $(function () {
                $('#id_time_penalty_pickers:has(input:not([readonly],[disabled]))').datetimepicker({"format": "mm"});
            });
        });

(function(window) {
    var callback = function() {
        $(function(){$("#id_contest_length_pickers:has(input:not([readonly],[disabled]))").datetimepicker({"language": "en-us", "format": "HH:MM"});});
    };
    if(window.addEventListener)
        window.addEventListener("load", callback, false);
    else if (window.attachEvent)
        window.attachEvent("onload", callback);
    else window.onload = callback;
})(window);