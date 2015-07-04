/**
 * Created by realityone on 15/7/4.
 */
$(document).ready(function () {
    $('form').submit(function () {
        var inputs = $(this).find('input[type="text"]');
        var can_submit = true;
        inputs.each(function () {
            if ($(this).attr('placeholder') == 'required' && $(this).val().length == 0) {
                can_submit = false;
                $(this).parent().addClass('has-error')
            }
        });
        return can_submit;
    });
});