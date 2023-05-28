var url_spanish = '../../static/lib/DataTables/js/spanish.txt'
var minDate, maxDate;

$.fn.dataTable.ext.search.push(
    function (settings, data, dataIndex) {
        var min = minDate.val();
        var max = maxDate.val();
        var date = new Date(data[1]);

        if (
            (min === null && max === null) ||
            (min === null && date <= max) ||
            (min <= date && max === null) ||
            (min <= date && date <= max)
        ) {
            return true;
        }
        return false;
    }
);

/***************************************************************/    

$(document).ready(function () {
    minDate = new DateTime($('#min'), {
        format: 'DD/MM/YYYY'
    });
    maxDate = new DateTime($('#max'), {
        format: 'DD/MM/YYYY'
    });   

/***************************************************************/    
    var table = $('#tabla').DataTable({
        "language": {
            url: url_spanish
        },
        responsive: true,
        dom: 'Bfrtilp',
        order: [[0, 'desc']],
        buttons: [{
            extend: 'excelHtml5',
            text: '<i class="bi bi-file-earmark-excel"></i>',
            titleAttr: 'Exportar a Excel',
            className: 'btn btn-success',
        }],
    });

    $('#min, #max').on('change', function () {
    table.draw();
    }); 

/***************************************************************/    

    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        $('form')[0].reset();
        $('#modal-create').modal('show');
    });


    $('.btnEdit').on('click', function () {
        var data = table.row($(this).parents('tr')).data();
        console.log(data);
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data[2]);

        $('input[name="name"]').val(data[3]);
        $('input[name="dni"]').val(data[4]);
        $('input[name="gender"]').val(data[5]);

        $('#modal-edit').modal('show');
    });
   
    
    $('.btnDel').on('click', function () {
        var data = table.row($(this).parents('tr')).data();
        var parameters = new FormData();
        parameters.append('action','delete');
        parameters.append('id', data[2]);
        jqueryconfirm(window.location.pathname, 'Notificacion', 'Estas seguro que desea eliminar?', parameters, function () {
            window.location.reload();
        });
    });


    $('#Form-form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        jqueryconfirm(window.location.pathname, 'Notificacion', 'Estas seguro que desea guardar?', parameters, function () {
            $('#modal-create').modal('hide');
            window.location.reload();
        });
    });
}); 