$(document).ready(function() {
    var today = new Date();
    var minBirthDate = new Date(today.getFullYear() - 13, today.getMonth(), today.getDate());

    $('#dob').datepicker({
        dateFormat: 'yy-mm-dd',
        changeMonth: true,
        changeYear: true,
        maxDate: '-13y',
        yearRange: '1920:' + today.getFullYear()
    });
});