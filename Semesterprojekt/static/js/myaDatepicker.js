$(document).ready(function() {
    // each input field with the class timepicker gets a datetimepicker with only time fields
    $('input.timepicker').each(function () {
        $(this).datetimepicker({
            locale: 'de',
            sideBySide: true,
            format: 'LT'
        });
    });
    // each input field with the class datetimepicker gets a datetimepicker
    $('input.datetimepicker').each(function () {
        $(this).datetimepicker({
            locale: 'de',
            sideBySide: true
        });
    });
});