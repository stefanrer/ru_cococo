$(document).ready(function () {

    const langChangeButton = $('#language-switch');

    if (langChangeButton.attr('data-lang') === 'en') {
        $('#original').hide();
        $('#translated').show();
    } else {
        $('#original').show();
        $('#translated').hide();
    }

    langChangeButton.click(function () {
        if (langChangeButton.attr('data-lang') === 'en') {
            $('#original').show();
            $('#translated').hide();
        } else {
            $('#original').hide();
            $('#translated').show();
        }
    })
});