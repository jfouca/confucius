$(function() {
    $('.datepicker').datepicker({
        dateFormat: 'yy-mm-dd',
    });
    $('#toggle_modal').modal({
        show: 0,
    });
    $('#toggle_conference').click(function() {
        $('#toggle_modal').modal('show');
        return false;
    });
});
