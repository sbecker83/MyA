$(document).ready(function() {
    $('#data-table').DataTable( {
        columnDefs: [{
            orderable: false,
            targets: "no-sort"
        }],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/German.json"
        }
    });
});