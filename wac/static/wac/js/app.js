// $('.card').on( 'click', function( event ) {
//      let title = $( this ).find( '.card-title' ).text();
//      let theModal = $( "#myModal" );
//      console.log('trying');
//      console.log(title)
//
//      if ( title == "Create New Chore" ) {
//           theModal.find( '.modal-title' ).text( 'Create A New Chore' );
//           theModal.find( '#title' ).val( '' );
//           theModal.find('#duration').val( '' );
//           theModal.find( '#frequency' ).val( '' );
//
//      } else {
//           theModal.find( '.modal-title' ).text( 'Edit:' );
//
//           theModal.find( '#title' ).val( title );
//
//           let duration = $( this ).find( '.cardDuration' ).text();
//           theModal.find('#duration').val( duration );
//
//           let freq = $( this ).find( '.cardFrequency' ).text();
//           theModal.find( '#frequency' ).val( freq );
//
//
//      }
//
//      theModal.modal('toggle');
// });


$(".alert").fadeTo(3500, 0).slideUp(500, function(){
    $(this).remove();
});

var form_options = { target: '#modal', success: function(response) {} };
$('#chore_edit').ajaxForm(form_options);
