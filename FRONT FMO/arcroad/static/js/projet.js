$(function () {

  var listeProjets = $('#listeProjets').DataTable( {
      paging:   true,
      info:     true,
      searching: true,
      ajax: API_URL+'projets',
      columns: [
            { "data": "projectName" },
            { "data": "projectClient" },
            { "data": "projectCPI" },
            { "data": "projectDP" },
            { "data": "projectDataMEP" },
            { "data": "projectGed" },
            { "data": "projectId" },
        ],
      columnDefs: [ {
            "targets": -1,
            "render": function(data){
              return data
            }
        } ]
  } );

  $(document).on('click', '#createProjet', function () {
    $('#modal_formulaire').modal('show');
    $('#modal_formulaire_label').empty()
    $('#modal_formulaire_label').append('Nouveau projet')
    $.ajax({
       url : '/formCreateProjet',
       type : 'GET',
       dataType : 'html',
       success : function(code_html, statut){
         $('#modal_formulaire_body').empty()
         $('#modal_formulaire_body').append(code_html)
         $.ajax({
           url : API_URL+'users',
           success : function(json, statut){
             for (i in json.data){
               console.log("<option idDP="+json.data[i].userId+">"+json.data[i].userPrenom+" "+json.data[i].userNom+"</option>")
               $('#selectDP').append("<option idDP='"+json.data[i].userId+"'>"+json.data[i].userPrenom+" "+json.data[i].userNom+"</option>")
             }
           }
         });

         //On charge la liste des clients

       } //fin du success
    });
  });




});
