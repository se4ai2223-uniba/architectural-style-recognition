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
      upload(input.files[0])
  
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
  

  const upload = (file) =>{
    let formData = new FormData();
    formData.append("imgfile", file);
    var paragraph = document.getElementById("prediction");
    fetch('http://localhost:81/classify_image/', { // Your POST endpoint
      method: 'POST',
      headers: {
        // Content-Type may need to be completely **omitted**
        // or you may need something
      },
      body: formData // This is your file object
    }).then(
      response => response.json() // if the response is a JSON object
    )
    .then(
      success => {console.log(success['label']) // Handle the success response object
      label = success['label'];
      id_image = success['id'];
      var text = document.createTextNode("This building looks like " + label +" style")
      paragraph.appendChild(text)
    }).catch(
      error => console.log(error) // Handle the error response object
    );
  };


  async function uploadNewClass(){
    var newLabel = document.getElementById("new_label");
    var value = newLabel.value;
    console.log("New class: "+value+ " ID image: "+id_image)
    fetch('http://localhost:81/feedback_class/?id_img='+parseInt(id_image)+'&new_class='+parseInt(value), {
    method: 'PUT',
    headers: {},
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
      $("#fail").addClass("show");
    });
  }

  $(function() {
    $(".btn-close").click(function() {
       $(this).closest(".alert").hide();         
   });
});