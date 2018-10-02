function addPostVotes(postId, klass, vote){
  $('#'+postId+'_vote').unbind('click').click(function(){return false;});
  $.getJSON("/votes/add_post_vote",
            { post: postId, klass: klass, vote: vote },
           function(json){
              if(json.success){
                 $('#'+postId+'_rating')
                      .removeClass()
                      .addClass(json.vote_class)
                      .attr("innerHTML",json.rating);
                 $('#'+postId+'_rating_up')
                      .attr('src', STATIC_URL + 'design/3/img/b-bar/plus_disabled.png');
              }
              if(json.error){
                 alert(json.error)
              }
              return false;
           });

  return false;
}


function set_name(){
  $.getJSON("/ajax/set_name", { name: $('#set_name_form #id_name').attr('value') },
           function(json){
              if(json.success){
                 $('#set_name_form .js-result').text('Имя изменено');
              }
              if(json.error){
                 $('#set_name_form .js-result').text('Ошибка: ' + json.error);
              }
              return false;
           });

  return false;
}

function set_news(){
  $.getJSON("/ajax/set_news", { news: $('#set_news_form #id_news').attr('checked') },
           function(json){
              if(json.success){
                 $('#set_news_form .js-result').text('Настройки сохранены');
              }
              if(json.error){
                 $('#set_news_form .js-result').text('Ошибка: ' + json.error);
              }
              return false;
           });
  return false;
}
