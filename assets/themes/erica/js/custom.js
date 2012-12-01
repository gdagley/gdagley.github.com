
/* Twitter */

/* Twitter #1 */

jQuery(function($){
   $(".tweet").tweet({
      username: "gdagley",
      join_text: "auto",
      avatar_size: 0,
      count: 5,
      auto_join_text_default: "I said,",
      auto_join_text_ed: "I",
      auto_join_text_ing: "I was",
      auto_join_text_reply: "I replied to",
      auto_join_text_url: "I was checking out",
      loading_text: "loading tweets...",
      template: "{time} {text}"
   });
});

/* Twitter #2 */

jQuery(function($){
   $(".ctweet").tweet({
      username: "gdagley",
      join_text: "auto",
      avatar_size: 0,
      count: 1,
      auto_join_text_default: "we said,",
      auto_join_text_ed: "we",
      auto_join_text_ing: "we were",
      auto_join_text_reply: "we replied to",
      auto_join_text_url: "we were checking out",
      loading_text: "loading tweets...",
      template: "{text}"
   });
});

/* Github */

jQuery(function($){
 $('#ghw').githubWidget({
   username: 'gdagley',
   firstCount: 5
 });
});

/* Support list */

$("#slist a").click(function(e){
   e.preventDefault();
   $(this).next('p').toggle(200);
});

/* Portfolio */

// filter items when filter link is clicked
$('#filters a').click(function(){
  var selector = $(this).attr('data-filter');
  $container.isotope({ filter: selector });
  return false;
});


jQuery("a[class^='prettyPhoto']").prettyPhoto({
overlay_gallery: false, social_tools: false
});
