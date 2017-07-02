$(document).ready(function() {
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