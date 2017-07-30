//==========================================================================
//            MESSAGES                                                 //
//==========================================================================

$(".alert-success").fadeTo(3500, 0).slideUp(500, function(){
    $(this).remove();
});

$(".alert-info").fadeTo(3500, 0).slideUp(500, function() {
    $(this).remove();
});

// $(".alert-warning").fadeTo(3500, 0).slideUp(500, function(){
//     // $(this).remove();
// });

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
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/wac/lineup/make/',
        type: 'POST',
        data: { csrfmiddlewaretoken : csrftoken, pk : theAssPK,
    },
    success : function(data) {
        let path = $('#' + theAssPK).css('background-image');
        if (~path.indexOf('YES')) {
            path = path.replace('YES', 'NO');
        } else {
            path = path.replace('NO', 'YES');
        }
        $('#' + theAssPK).css('background-image', path);

        $('#server_response').html(data);
    }
});
}

//==========================================================================
//            FOR ALL MODALS                                              //
//==========================================================================

function find_modal(theUrl) {
    var modal = $('.modal');
    var url = window.location.href;
    $.ajax({
        url: theUrl,
        context: document.body
    }).done(function(response) {
        modal.html(response);
        if ($(modal).find('#id_fromUrl')) {
            $(modal).find('#id_fromUrl').val(url);
        }
    });

    // For Chore Modal only
    if (url === 'https://whatachore.herokuapp.com/wac/chores') {
        checkDOMChange();
    }
}

//  Icon Choices ------------------------------------------------------
function checkDOMChange() {
    // .chore-modal is on the div.modal-dialog which is not in orig DOM
    if ($('.chore-modal').length) {
        let theInput = $('input[name="chore_icon_location"]:checked');
        $(theInput).parent().parent().addClass('checked');
        $(theInput).parent().parent().css("border", "2px solid #C63D0F");
    } else {
        setTimeout( checkDOMChange, 100 );
    }
}

$('body').on('hidden.bs.modal', '#choreModal', function () {
    $(this).empty();
});

$(document).on('click', 'input:radio', function(event) {
    // remove checked from wherever it was
    $('.checked').css("border", "");
    $('.checked').css("border", "2px solid #FDF3E7"); // temp
    $('.checked').removeClass('checked');

    $(this).parent().parent().addClass('checked');  // this class might be handled in css
    $(this).parent().parent().css("border", ""); // temp
    $(this).parent().parent().css("border", "2px solid #C63D0F"); // temp

});
//  Icon Choices ------------------------------------------------------


// Modal Forms

function apply_form_field_error(modal, fieldname, error)
{
    var body = $(modal).find('.modal-body');
    if (fieldname === '__all__') {
        var input = body,
            container = body,
            error_msg = $('<p class="help-inline px-3 text-danger ajax-error">' + error + '</p>');
    } else {
        var input = $(modal).find('#id_' + fieldname),
            container = $(input).parent();
            error_msg = $('<p class="help-inline text-danger ajax-error">' + error[0] + '</p>');
    }

    container.addClass("error");
    // error_msg.append(container);
    input.after(error_msg);
}

function clear_form_field_errors(form) {
    $('.ajax-error', $(form)).remove();
    $('.error', $(form)).removeClass('error');
}

// For Multiple Modals
$(document).on('show.bs.modal', '.modal', function () {
    var zIndex = 1040 + (10 * $('.modal:visible').length);
    $(this).css('z-index', zIndex);
    setTimeout(function() {
        $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
    }, 0);
});

$(document).on('hidden.bs.modal', '.modal', function () {
    $('.modal:visible').length && $(document.body).addClass('modal-open');
});


//==========================================================================
//            RESET PASSWORD                                              //
//==========================================================================

$(document).on('submit', '.pw-reset-form', function(event) {
    event.preventDefault();
    postReset();
});

function postReset() {
    var frm = $('.pw-reset-form');
    clear_form_field_errors(frm);
    if ( $('#pw-reset-modal').length ) {
        var modal = $('#pw-reset-modal');
        var email = $(modal).find('#id_email').val();
        var errorContainer = modal;
    } else {
        var email = $('.pw-reset-form').find('#id_email').val()
        var errorContainer = $('.pw-reset-form')
    };

    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: $(frm).attr('action'),
        type: $(frm).attr('method'),
        data: $(frm).serialize(),
        success: function (data) {
            if (data.status === 'success') {
                location.reload();
            }
        },
    });
}


//==========================================================================
//            LOGIN MODAL                                                 //
//==========================================================================

$(document).on('submit', '.login-form', function(event) {
    event.preventDefault();
    postLogin();
});

function postLogin() {
    var frm = $('.login-form');
    clear_form_field_errors(frm);
    if ( $('#login-modal').length ) {
        var modal = $('#login-modal');
        var usrnm = $(modal).find('#id_username').val();
        var psswrd = $(modal).find('#id_password').val();
        var errorContainer = modal;
    } else {
        var usrnm = $('.login-form').find('#id_username').val();
        var psswrd = $('.login-form').find('#id_password').val();
        var errorContainer = $('.login-form');
    };

    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: $(frm).attr('action'),
        type: $(frm).attr('method'),
        data: {csrfmiddlewaretoken : csrftoken, 'username': usrnm, 'password': psswrd},
        success: function (data){
            if (data.status === 'success') {
                if ($(modal)) {
                    $(modal).modal('hide');
                }
                window.location.replace(data.url);
            } else {
                alert("success function, but data.status != success");
            }
        },
        error: function (data) {
            var errors = $.parseJSON(data.responseText);
            $.each(errors, function(index, value) {
                if (index === '__all__') {
                    apply_form_field_error(errorContainer, index, value[0])
                } else {
                    apply_form_field_error(errorContainer, index, value);
                }
            });
        }
    });
}


//==========================================================================
//           CREATE CHORE MODAL                                        //
//==========================================================================

$(document).on('submit', '.create-chore', function(event) {
    event.preventDefault();
    postCreateChore();
});

function postCreateChore() {
    var frm = $('.create-chore');
    clear_form_field_errors(frm);
    var modal = $('.modal');
    $.ajax({
        url: $(frm).attr('action'),
        type: $(frm).attr('method'),
        data: $(frm).serialize(),
        success: function (data) {
            if (data.status === 'success') {
                if (data.messages === 'welcoming') {
                    $(modal).modal('hide');
                    location.replace(data.url);
                } else {
                    $(modal).modal('hide');
                    location.reload();
                }
            } else {
                alert("success function, but data.status != success");
            }
        },
        error: function (data) {
            var errors = $.parseJSON(data.responseText);
            $.each(errors, function(index, value) {
                if (index === '__all__') {
                    apply_form_field_error(modal, index, value[0])
                } else {
                    apply_form_field_error(modal, index, value);
                }
            });
        }
    });
}



//==========================================================================
//           ACCOUNT SETTINGS FORM                                        //
//==========================================================================
$(document).on('submit', '.account_setting_change', function(event) {
    event.preventDefault();
    postChangeSettings();
});

function postChangeSettings() {
    var frm = $('.account_setting_change');
    clear_form_field_errors(frm);
    var modal = $('.modal');
    $.ajax({
        url: $(frm).attr('action'),
        type: $(frm).attr('method'),
        data: $(frm).serialize(),
        success: function (data) {
            $(modal).modal('hide');
            location.reload();
        }
    });
}


//==========================================================================
//           EMAIL WORKER MODAL                                           //
//==========================================================================
$(document).on('submit', '.email_to_worker', function(event) {
    event.preventDefault();
    postEmailWorker();
});

function postEmailWorker() {
    var frm = $('.email_to_worker');
    clear_form_field_errors(frm);
    var modal = $('.modal');
    $.ajax({
        url: $(frm).attr('action'),
        type: $(frm).attr('method'),
        data: $(frm).serialize(),
        success: function (data) {
            if (data.status === 'success') {
                $(modal).modal('hide');
                location.reload();
            } else {
                alert("success function, but resp_data != success");
            }
        },
        error: function (data) {
            var errors = $.parseJSON(data.responseText);
            $.each(errors, function(index, value) {
                if (index === '__all__') {
                    console.log('index == __all__');
                } else {
                    apply_form_field_error(modal, index, value);
                }
            });
        }
    });
}


//==========================================================================
//           PASSWORD CHANGE MODAL                                        //
//==========================================================================

$(document).on('submit', '.pw-change-form', function(event) {
    event.preventDefault();
    postChangePassword();
});

function postChangePassword() {
    var frm = $('.pw-change-form');
    clear_form_field_errors(frm);
    var modal = $('.modal');
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
                } else {
                    apply_form_field_error(modal, index, value);
                }
            });
        }
    });
};


//==========================================================================
//            IMAGE CROPPING                                              //
//==========================================================================

function closeThis() {
    $('#modalCrop').modal('hide');
}

$(function () {
    var $image;
    var cropBoxData;
    var canvasData;

    // Script to open the cropModal
    $(document).on('change', '#id_mugshot', function () {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#image').attr('src', e.target.result);
                $('#modalCrop').modal('show');
            }
            $image = $('#image');
            $imageSrc = $('#image').attr('src');
            reader.readAsDataURL(this.files[0]);
        }
    });

    // Script to handle the cropper box
    $(document).on('shown.bs.modal', '#modalCrop', function () {
        $image.cropper({
            viewMode: 1,
            aspectRatio: 3/4,
            movable: false,
            rotatable: true,
            zoomOnWheel: false,
            // minCropBoxWidth: 200,
            // minCropBoxHeight: 200,
            ready: function () {
                $image.cropper('setCanvasData', canvasData);
                $image.cropper('setCropBoxData', cropBoxData);
            }
        });
    }).on('hidden.bs.modal', '#modalCrop', function () {
        cropBoxData = $image.cropper('getCropBoxData');
        canvasData = $image.cropper('getCanvasData');
        $image.cropper('destroy');
    });

    // Script to collect the data and post to the server
    $(document).on('click', '.js-crop-and-upload', function () {
        var cropData = $image.cropper('getData');
        $('#id_x').val(cropData['x']);
        $('#id_y').val(cropData['y']);
        $('#id_height').val(cropData['height']);
        $('#id_width').val(cropData['width']);
        $('#id_rotate').val(cropData['rotate']);
        closeThis();
    });

    $(document).on('click', '.js-zoom-in', function () {
        $image.cropper('zoom', 0.1);
    });

    $(document).on('click', '.js-zoom-out', function () {
        $image.cropper('zoom', -0.1);
    });
});
