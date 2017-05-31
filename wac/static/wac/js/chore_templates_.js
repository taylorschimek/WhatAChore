function check_field_value(new_val) {
    console.log("function ran");
    console.log(new_val);
    if (new_val === 'Once' ||
        new_val === 'Daily' ||
        new_val === 'Every 2 Days' ||
        new_val === 'Every 3 Days') {
            // Hide id_subinterval
            $('.hiddenSub').prop('disabled', true);
    } else {
            // Show id_subinterval
            $('.hiddenSub').prop('disabled', false);
    }
}


$(document).ready(function() {
    let jenk = $('.hideController option:selected').val();
    console.log(jenk);
    check_field_value(jenk);

    $('.hideController').on('change', function(e) {
        console.log(e.currentTarget.value);
        check_field_value(e.currentTarget.value);
    });
})
