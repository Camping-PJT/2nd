document.addEventListener('DOMContentLoaded', function() {
  var bg = new Array();
  bg[bg.length] = '/static/image/main1.jpg';
  bg[bg.length] = '/static/image/main2.jpg';
  bg[bg.length] = '/static/image/main3.jpg';
  bg[bg.length] = '/static/image/main4.jpg';
  bg[bg.length] = '/static/image/main5.jpg';
  bg[bg.length] = '/static/image/main6.jpg';
  bg[bg.length] = '/static/image/main7.jpg';
  bg[bg.length] = '/static/image/main8.jpg';
  bg[bg.length] = '/static/image/main9.jpg';
  bg[bg.length] = '/static/image/main10.jpg';

  var obj = document.getElementById('backGround');
  var size = Math.floor(Math.random() * bg.length);
  j = (isNaN(size)) ? 0 : size;
  obj.style.backgroundImage = 'url(' + bg[size] + ')';
});

