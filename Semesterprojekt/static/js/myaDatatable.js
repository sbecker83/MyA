$(document).ready(function() {
    // the parsing of the used (german) datetime format needs to be set, so sorting of dates is possible
    $.fn.dataTable.moment('DD.MM.YYYY HH:mm');
    $('.data-table').each(function () {
        $(this).DataTable( {
            columnDefs: [{
                orderable: false,
                targets: "no-sort"
            }],
            "language": {
                "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/German.json"
            }
        });
    });
});