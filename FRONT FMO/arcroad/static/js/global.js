$(function () {

  // Varaible globale
  API_URL = 'http://192.168.30.21:5000/'


  // On intercepte le lien logout
  $('a[id=id_logout]').on("click", function(){
        $.get($(this).attr('page'),{}, function (data) {
          window.location.replace("/login")
      });
  });


  // La modal pour afficher les retours
  $("#modal_alerte").modal('hide');
  $("#modal_question").modal('hide');


  // Interception du form de login.
  // SUCCESS : On récupère un token JWT et on charge le template de base
  $("#login_form").submit(function(e){
    e.preventDefault();
    $.ajax({
     url: '/login',
     type: 'POST',
     dataType: 'json',
     data: $(this).serialize(),
     success:function(response){
        window.location.replace("/index");
      }
    });
  });


});
