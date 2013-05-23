function addPostVotes(postId, klass, vote){
  $('#'+postId+'_vote').unbind('click').click(function(){return false;});
  $.getJSON("/ajax/add_post_vote",
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


function addComment(postId, klass, commentId){
  comment = $('#content'+commentId).attr('value');
  if( !comment ){ return false; }

  $.getJSON("/ajax/add_comment",
            { comment: commentId, klass: klass, post: postId, content: comment},
           function(json){
              if(json.success){
                 $('#aftercomment'+json.afterComment)
                     .after(json.html);
                 init();
              }
              if(json.error){
                 alert(json.error)
              }
              return false;
           });

  $('#commentform'+commentId).hide();
  $('#content'+commentId).attr('value', '');
  $('#commentlink'+commentId).show();
  return false;
}

function addPicLink(insertMode, fieldId, picId){
    // Вставляет в поле редактирования ссылку <glader pic="...">
    field = $('#'+fieldId);
    field.text( field.text() + '<glader pic="' + picId + '">' );
}

function setBestAnswer(commentId){
 $.getJSON("/ajax/best_answer",
            { comment: commentId},
           function(json){
              if(json.success){
                 window.location = window.location;
              }
              if(json.error){
                 alert(json.error)
              }
              return false;
           });

  $('#best_answer_mark_'+commentId).hide();
  return false;
}

function delBestAnswer(commentId){
 $.getJSON("/ajax/best_answer",
            { comment: commentId, del:1 },
           function(json){
              if(json.success){
                 window.location = window.location;
              }
              if(json.error){
                 alert(json.error)
              }
              return false;
           });

  $('.js-del_best_answer').hide();
  return false;
}

function add_friend(friend_name){
 $.getJSON("/ajax/add_friend",
            { user: friend_name },
           function(json){
              if(json.success){
              	$('#add_friend').hide();
              	$('#cancel_friend').show();
              }
              if(json.error){
                 alert(json.error)
              }
              return false;
           });
  return false;
}

function cancel_friend(friend_name){
 if( confirm("Вы уверены, что хотите убрать его из друзей?")){
	 $.getJSON("/ajax/cancel_friend",
	            { user: friend_name },
	           function(json){
	              if(json.success){
	              	$('#cancel_friend').hide();
	              	$('#add_friend').show();
	              }
	              if(json.error){
	                 alert(json.error)
	              }
	              return false;
	           });
	  }
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

function addVKComment(num, last_comment, date, sign){
  $.getJSON("/ajax/add_vk_comment",
            {klass: klass, post: post_id, content: last_comment});
}

function pictureBox(picture_id, action){
  $.getJSON("/ajax/picturebox", {picture_id: picture_id, action: action},
           function(json){
              if(action == 'good'){
                 window.location = $('#picturebox_picture a').attr('href');
              };
              if(json.success){
                  $('#picturebox_picture').html(json.preview);
                  $('#picturebox_link_bad').unbind('click').click(function(event){
                      event.preventDefault();
                      pictureBox(json.picture_id, 'bad')
                  })
                  $('#picturebox_link_next').unbind('click').click(function(event){
                      event.preventDefault();
                      pictureBox(json.picture_id, 'next')
                  })
                  $('#picturebox_picture a').unbind('click').click(function(event){
                      event.preventDefault();
                      pictureBox(json.picture_id, 'good');
                  })
               }
              if(json.error){
                 alert(json.error);
              }
              return false;
           });
  return false;
}
