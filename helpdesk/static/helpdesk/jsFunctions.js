/**
 * Created by Серж on 25.04.2017.
 */
   function MyFunction(category) {
    $("#carousel-example-generic").carousel("next");
    // $( "a:hidden" ).show("slow")
    $("#id_category").val(category);
}


//user-profile

function editProfile(){
       $('.user-info').toggleClass('profile-hidden');
              $('.edit-user, .edit-user-form').toggleClass('profile-hidden');

       // $('.profile-fullname').val($('.profile-fullname').html());
       // $('.profile-fullname').toggleClass();
}
function editUserSubmit(){
    alert('xd');
    // $('.edit-user').hide();
    // $('.user-info').show();
}