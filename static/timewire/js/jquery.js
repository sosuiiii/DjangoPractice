// <script>
// 読み込めていない
  $(function(){
  $('.p, .i').css('opacity','0');
  $(window).scroll(function(){
    $('.effect').each(function(){
        // 要素の画面上部からの距離▼
      var imgPos = $(this).offset().top;
      // スクロール量▼
      var scroll = $(window).scrollTop();
      // ウィンドウの高さ▼
      var windowHeight = $(window).height();
      // 1/1.7、つまり下から0.58の比率の位置が発動分岐点▼
      if(scroll > imgPos - windowHeight + windowHeight/1.7){
        $('.i,.p',this).css('opacity','1');
      }else{
        $('.i,.p',this).css('opacity','0');
      }
    });
  });
  });
// </script>