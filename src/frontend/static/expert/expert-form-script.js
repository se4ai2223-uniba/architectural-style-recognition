var id_image
var new_label

function readURL(input) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();

    reader.onload = function (e) {
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


const upload = (file) => {
  let formData = new FormData();
  formData.append("imgfile", file);

  var paragraph = document.getElementById("prediction");

  var settings = {
    "url": "http://localhost:9100/classify_image/",
    "method": "POST",
    "timeout": 0,
    "processData": false,
    "mimeType": "multipart/form-data",
    "contentType": false,
    "data": formData
  };

  $.ajax(settings).done(function (response) {
    console.log(response);
    res = JSON.parse(response);

    label = res['label'];
    id_image = res['id'];
    var text = document.createTextNode("This building looks like " + label)
    paragraph.appendChild(text)
  });

  //  fetch("http://archinet-se4ai.ddns.net:9100/classify_image/", { // Your POST endpoint
  //    requestOptions
  //  }).then(
  //    response => response.json() // if the response is a JSON object
  //  )
  //    .then(
  //      success => {
  //        console.log(success['label']) // Handle the success response object
  //        label = success['label'];
  //        id_image = success['id'];
  //        var text = document.createTextNode("This building looks like " + label + " style")
  //        paragraph.appendChild(text)
  //      }).catch(
  //        error => console.log(error) // Handle the error response object
  //      );
};


async function uploadNewClass() {
  var newLabel = document.getElementById("new_label");
  var value = newLabel.value;
  console.log("New class: " + value + " ID image: " + id_image)


  var settings = {
    "url": "http://localhost:9100/feedback_class/?id_img=" + parseInt(id_image) + '&new_class=' + parseInt(value),
    "method": "PUT",

  };

  $.ajax({
    url: "http://localhost:9100/feedback_class/?id_img=" + parseInt(id_image) + '&new_class=' + parseInt(value),
    method: "PUT",
    headers: { 'Accept': 'application/json' }
  }
  ).done(function (response) {
    console.log(response);
  });

  $.ajax(settings).done(function (response) {
    console.log(response);
  });

  //fetch('http://localhost:9100/feedback_class/?id_img=' + parseInt(id_image) + '&new_class=' + parseInt(value), {
  //  method: 'PUT',
  //}).then(
  //  response => {
  //    console.log(response.status);
  //    response.json();
  //    if (response.status == '200')
  //      $("#success").addClass("show");
  //    else
  //      $("#fail").addClass("show");
  //  }
  //).then(
  //  data => console.log(data)
  //).then(
  //  success => {
  //    console.log("Success: " + success);
  //  }).catch(
  //    error => {
  //      console.log("error:" + error);
  //      $("#fail").addClass("show");
  //    });

}

$(function () {
  $(".btn-close").click(function () {
    $(this).closest(".alert").hide();
  });
});