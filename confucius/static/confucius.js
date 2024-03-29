function confucius() {
    if ($('.sorted-datatable tr').length > 2){
        $('.sorted-datatable').dataTable({
            sDom: "<'row'<'span5'l><'span5'f>r>t<'row'<'span5'i><'span5'p>>",
            bStateSave: true,
            sPaginationType: 'bootstrap',
            oLanguage: {
                sLengthMenu: '_MENU_ records per page'
            }
        });
    }

    $('.datepicker').datepicker({
        dateFormat: 'yy-mm-dd',
    });
    $('.toggle_modal').modal({
        show: 0
    });
    $('.toggle_conference').click(function() {
        $(this).next().modal('show');
        return false;
    });
    $('.assignments_finalize').click(function() {
        $(this).next().modal('show');
        return false;
    });
    $('.tooltip-show').tooltip();
    $('.row-actions').live('mouseover', function() {
        $(this).find('.data-actions').removeClass('v-hidden');
    });
    $('.row-actions').live('mouseout', function() {
       $(this).find('.data-actions').addClass('v-hidden');
    });
    $('.dropdown-menu').find('a').hover(function() {
            $(this).find('[class^="icon"]').toggleClass('icon-white');
        }, function() {
            $(this).find('[class^="icon"]').toggleClass('icon-white');
        }
    );
    $('.top-alert').delay(10000);
    $('.top-alert').slideUp(function() {
        $(this).remove();
    });
    
    $('.collapse').on('hidden', function () {
        var $icon = $(this).closest('.accordion-group').find('.icon');
        $icon.toggleClass('icon-chevron-up')
        $icon.toggleClass('icon-chevron-down');
    });
    $('.collapse').on('shown', function () {
        var $icon = $(this).closest('.accordion-group').find('.icon');
        $icon.toggleClass('icon-chevron-up')
        $icon.toggleClass('icon-chevron-down');
    });
};

$(document).ready(confucius());
