var id_image
var new_label

function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function(e) {
        $('.image-upload-wrap').hide();
        $('.file-upload-image').attr('src', e.target.result);
        $('.file-upload-content').show();
        $('.image-title').html(input.files[0].name);
      };
      reader.readAsDataURL(input.files[0]);
    } else {
      removeUpload();
    }
  }
  
  function removeUpload() {
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
  }
  $('.image-upload-wrap').bind('dragover', function () {
          $('.image-upload-wrap').addClass('image-dropping');
      });
      $('.image-upload-wrap').bind('dragleave', function () {
          $('.image-upload-wrap').removeClass('image-dropping');
  });
  

  
  async function uploadNewImage(){

    var imageFile = document.getElementById("image_to_predict").files[0];

    let formData = new FormData();
    formData.append("imgfile", imageFile);

    var newLabel = document.getElementById("new_label");
    var value = newLabel.value;

    console.log(imageFile, value)

    fetch('http://localhost:9100/extend_dataset/?label='+parseInt(value), {
    method: 'POST',
    headers: {},
    body: formData,
    }).then(
      response => {
        console.log(response.status);
        response.json();
        if (response.status == '200')
          $("#success").addClass("show");
        else
          $("#fail").addClass("show");
      }
    ).then(
      data => console.log(data)
    ).then(
      success => {console.log("Success: " +success);
    }).catch(
      error => {console.log("error:"+error);
    });
  }


  $(function() {
    $(".btn-close").click(function() {
       $(this).closest(".alert").hide();         
   });
});