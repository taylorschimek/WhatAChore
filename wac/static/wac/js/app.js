
function find_modal(theUrl) {
    var modal = $('.modal');
    console.log(modal);
    $.ajax({
        url: theUrl,
        context: document.body
    }).done(function(response) {
        modal.html(response);
    });
    console.log('yep');

}


$(".alert").fadeTo(3500, 0).slideUp(500, function(){
    $(this).remove();
});

var form_options = { target: '#modal', success: function(response) {} };
$('#chore_edit').ajaxForm(form_options);


//For getting CSRF token
function getCookie(name) {
       var cookieValue = null;
       if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
         var cookie = jQuery.trim(cookies[i]);
         // Does this cookie string begin with the name we want?
         if (cookie.substring(0, name.length + 1) == (name + '=')) {
             cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
             break;
          }
     }
 }
 return cookieValue;
}

function assignmentDone(theAssPK) {
    console.log(theAssPK + ' is changing')

    var csrftoken = getCookie('csrftoken');

    $.ajax({
        url: '/wac/lineup/make/',
        type: 'POST',
        data: { csrfmiddlewaretoken : csrftoken, pk : theAssPK,
    },
    success : function(data) {
        console.log('success');
        let path = $('#' + theAssPK).css('background-image');
        if (~path.indexOf('YES')) {
            path = path.replace('YES', 'NO');
        } else {
            path = path.replace('NO', 'YES');
        }
        $('#' + theAssPK).css('background-image', path);

        $('#server_response').html(data);
    },
    error : function() {
        console.log('unsuccess');
    }
});
}
