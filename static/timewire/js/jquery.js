// <script>
// 読み込めていない
  $(function(){
  $('.p, .i').css('opacity','0');
  $(window).scroll(function(){
    $('.effect').each(function(){
      var imgPos = $(this).offset().top;
      var scroll = $(window).scrollTop();
      var windowHeight = $(window).height();
      // ▼1/1.7、つまり下から0.58の比率の位置が発動分岐点▼
      if(scroll > imgPos - windowHeight + windowHeight/1.7){
        $('.i,.p',this).css('opacity','1');
      }else{
        $('.i,.p',this).css('opacity','0.1');
      }
    });
  });
  });
// </script>