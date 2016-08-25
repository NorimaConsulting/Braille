$(document).ready(function() {
  $('select').material_select();

  $('.checkForInput').change(function() {
    checkFormState();
  })

  $("#inputText").on('input',function(e){
     checkFormState();
  });

  var downloadButton = $("#download-button");
  downloadButton.click(function() {
    if(!downloadButton.hasClass("disabled"))
    {
      var text = $("#inputText").val();
      var fontSize = $('input[name=size]:checked').val() ;
      var backPlate = $('input[name=backPlate]:checked').val() ;

      var fileName = text + ".stl"

      var URL = "/create"
      var data = {
        "text":encodeURIComponent(text),
        "fontSize":fontSize,
        "backPlate":backPlate
      }
      Materialize.toast('Downloading...', 4000)
      $.get( URL,data, function( data ) {
        download(data, fileName);
      }).error(function(err) {
        Materialize.toast('Failed to Download', 4000)
      });
    }

  });

});



function checkFormState() {

  var good = backOptionsIsFilledIn() && fontSizeIsFilledIn() && textIsGood();


  var downloadButton = $("#download-button");
  if(good){
    downloadButton.removeClass("disabled")
  }else{
    downloadButton.addClass("disabled")
  }

  return good;

}


function backOptionsIsFilledIn() {

  var value = $('input[name=backPlate]:checked').val() ;
  return typeof value != "undefined"
}

function fontSizeIsFilledIn() {
  var value = $('input[name=size]:checked').val() ;
  return typeof value != "undefined"
}

function textIsGood() {
  var value = $("#inputText").val();

  return value.length>0;
}
