
function find_modal(theUrl) {
    var modal = $('.modal');
    console.log(modal);
    $.ajax({
        url: theUrl,
        context: document.body
    }).done(function(response) {
        modal.html(response);
    });
}


$(".alert").fadeTo(3500, 0).slideUp(500, function(){
    $(this).remove();
});

var form_options = { target: '#modal', success: function(response) {} };
$('#chore_edit').ajaxForm(form_options);
