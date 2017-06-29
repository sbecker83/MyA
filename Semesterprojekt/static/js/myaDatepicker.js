$(document).ready(function() {
    // each input field with the class datetimepicker gets a datetimepicker
    $('input.datetimepicker').each(function () {
        $(this).datetimepicker({
            locale: 'de',
            sideBySide: true,
        });
    });
});