$(document).ready(
    
        $('.datepicker').datepicker({
            dateFormat: 'yy-mm-dd',
        }),
        $('.toggle_modal').modal({
            show: 0,
        }),
        $('.toggle_conference').click(function() {
            $(this).next().modal('show');
            return false;
        }),
        $('.assignments_finalize').click(function() {
            $(this).next().modal('show');
            return false;
        }),
        $('.tooltip-show').tooltip(),
        $('.row-actions').mouseenter(function() {
                $(this).find('.data-actions').toggleClass('v-hidden');
            }
        ),
        $('.row-actions').mouseleave(function() {
                $(this).find('.data-actions').toggleClass('v-hidden');
            }
        ),
        $('.dropdown-menu').find('a').mouseenter(function() {
                $(this).find('[class^="icon"]').toggleClass('icon-white');
            }
        ),
        $('.dropdown-menu').find('a').mouseleave(function() {
                $(this).find('[class^=["icon"]').toggleClass('icon-white');
            }
        ),
        $('#messages').delay(10000),
        $('#messages').fadeTo(2000, 0, function() {
            $('#messages').remove();
        })
);
