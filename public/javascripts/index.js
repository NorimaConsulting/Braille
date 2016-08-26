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

      var URL = "/create?text="+text+"&fontSize="+fontSize+"&backPlate=" + backPlate + ""

      Materialize.toast('Downloading...', 4000)
      $.get( URL, function( data ) {
        test_blob = convertBase64ToBlob(data, "application/sla")

        download(test_blob, fileName)
      }).error(function(err) {
        Materialize.toast('Failed to Download', 4000)
      });
    }

  });

});

function convertBase64ToBlob (base64String, contentType) {
  contentType = contentType || '';
  var sliceSize = 512;

  var byteCharacters = atob(base64String);
  var byteArrays = [];

  for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
    var slice = byteCharacters.slice(offset, offset + sliceSize);

    var byteNumbers = new Array(slice.length);
    for (var i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i);
    }

    var byteArray = new Uint8Array(byteNumbers);

    byteArrays.push(byteArray);
  }

  var blob = new Blob(byteArrays, {type: contentType});
  return blob;
}



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
