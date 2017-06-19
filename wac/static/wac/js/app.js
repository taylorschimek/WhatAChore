
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

//=====================================
//      modal form submit stuff      //
//=====================================

function apply_form_field_error(modal, fieldname, error)
{
    console.log('apply called');
    console.log(modal);
    console.log(fieldname);
    var body = $(modal).find('.modal-body');
    if (fieldname === '__all__') {
        console.log('use error');
        console.log(error);
        var input = body,
            container = body,
            error_msg = $('<p class="help-inline px-3 text-danger ajax-error">' + error + '</p>');
    } else {
        console.log('use error[0]');
        console.log(error[0]);
        var input = $(modal).find('#id_' + fieldname),
            container = $(input).parent();
            error_msg = $('<p class="help-inline text-danger ajax-error">' + error[0] + '</p>');
    }

    console.log('id_' + fieldname);
    console.log(error_msg);
    console.log(container);
    console.log(input);
    container.addClass("error");
    // error_msg.append(container);
    input.after(error_msg);
}

function clear_form_field_errors(form) {
    $('.ajax-error', $(form)).remove();
    $('.error', $(form)).removeClass('error');
}

$(document).on('submit', '.login-form', function(event) {
    event.preventDefault();
    postLogin();
});

function postLogin() {
    var frm = $('.login-form');
    clear_form_field_errors(frm);
    console.log($(frm).serialize())
    var modal = $('#login-modal');
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: $(frm).attr('action'),
        type: $(frm).attr('method'),
        data: {csrfmiddlewaretoken : csrftoken, 'username': $('#loginModal').find('#id_username').val(), 'password': $('#loginModal').find('#id_password').val()},
        success: function (data){
            if (data.status === 'success') {
                $(modal).modal('hide');
                window.location.replace(data.url);
            } else {
                alert("success function, but data.status != success");
            }
        },
        error: function (data) {
            console.log("error");
            console.log(data)
            var errors = $.parseJSON(data.responseText);
            $.each(errors, function(index, value) {
                console.log(value);
                if (index === '__all__') {
                    console.log('index == __all__');
                    apply_form_field_error(modal, index, value[0])
                } else {
                    console.log('index != __all__');
                    apply_form_field_error(modal, index, value);
                }
            });
        }
    });
}


$(document).on('submit', '.pw-change-form', function(event) {
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    postChangePassword();
});

function postChangePassword() {
    // console.log('postChangePassword is working');
    var frm = $('.pw-change-form');
    clear_form_field_errors(frm);
    var modal = $('#homeModal');
    $.ajax({
        url: $(frm).attr('action'),
        type: $(frm).attr('method'),
        data: $(frm).serialize(),
        success: function (data) {
            if (data.status === 'success') {
                $(modal).modal('hide');
                location.reload();
            } else {
                alert("success function, but data.status != success");
            }
        },
        error: function (data) {
            var errors = $.parseJSON(data.responseText);
            $.each(errors, function(index, value) {
                if (index === '__all__') {
                    console.log('index == __all__');
                    // apply_form_field_error(index, value);
                    // alert(error);
                    // django_message(value[0], 'error');
                } else {
                    console.log('index != __all__');
                    apply_form_field_error(modal, index, value);
                }
            });
        }
    });
};
