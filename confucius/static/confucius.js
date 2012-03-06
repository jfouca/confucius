$(document).ready(
    $(function() {
        $('.datepicker').datepicker({
            dateFormat: 'yy-mm-dd',
        });
        $('.toggle_modal').modal({
            show: 0,
        });
        $('.toggle_conference').click(function() {
            $(this).next().modal('show');
            return false;
        });
        $('.tooltip-show').tooltip();
        $('.row-actions').mouseenter(function() {
                $(this).find('.data-actions').toggleClass('v-hidden');
            }
        ),
        $('.row-actions').mouseleave(function() {
                $(this).find('.data-actions').toggleClass('v-hidden');
            }
        );
    })
);
