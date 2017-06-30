$(document).ready(function() {
    // each input field with the class datetimepicker gets a datetimepicker
    $('input.timepicker').each(function () {
        $(this).datetimepicker({
            locale: 'de',
            sideBySide: true,
            format: 'LT'
        });
    });
    $('input.datetimepicker').each(function () {
        console.log("hallo");
        $(this).datetimepicker({
            locale: 'de',
            sideBySide: true
        });
    });
});