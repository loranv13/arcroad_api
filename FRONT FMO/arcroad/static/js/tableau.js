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


});
