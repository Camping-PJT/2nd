// 파일 선택시, 이미지 미리보기
$(document).ready(function() {
  function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function(e) {
        $("#profile-image-preview").attr("src", e.target.result);
        $("#profile-image-preview").show();
      }

      reader.readAsDataURL(input.files[0]);
    }
  }

  $("#id_profile_image").change(function() {
    readURL(this);
  });
});