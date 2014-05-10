//additional properties for jQuery object
$(document).ready(function(){
   //align element in the middle of the screen
   $.fn.alignCenter = function() {
      //get margin left
      var marginLeft =  - $(this).width()/2 + 'px';
      //get margin top
      //var marginTop =  - $(this).height()/2 + 'px';
      var marginTop =  ($(window).height()/2 ) - ( $("#popup").height()/2) + 'px';
      //return updated element
      return $(this).css({'margin-left':marginLeft, 'top':marginTop});
   };

   $.fn.togglePopup = function(){
     //detect whether popup is visible or not
     if($('#popup').hasClass('g-hidden'))
     {
       //hidden - then display
       if($.browser.msie)
       {
         $('#opaco').height($(document).height()).toggleClass('g-hidden')
                    .click(function(){$(this).togglePopup();});
       }
       else
       //in all the rest browsers - fade slowly
       {
         $('#opaco').height($(document).height()).toggleClass('g-hidden').fadeTo('slow', 0.7)
                    .click(function(){$(this).togglePopup();});
       }

       $('#popup_iframe').alignCenter().toggleClass('g-hidden');

        popup = $('#popup');
        popup
          .html($(this).html())
          .alignCenter()
          .toggleClass('g-hidden')
          .before('<iframe id="popup_iframe"></iframe>');
        $('#popup_iframe')
          .css('border', 0)
          .css('margin-left', popup.css('margin-left'))
          .css('top', popup.css('top'))
          .css('width', popup.css('width'))
          .css('height', popup.css('height'));
     }
     else
     {
       //visible - then hide
       $('#opaco').toggleClass('g-hidden').removeAttr('style').unbind('click');
       $('#popup').toggleClass('g-hidden').html('');
       $('#popup_iframe').remove();
     }
   };
});

function switchAuthForms(){
    $('#login_form_block').toggleClass('g-hidden');
    $('#registration_form_block').toggleClass('g-hidden');
    return false;
}

function submitLoginForm(event){
    login = $('#login_form #id_login').val();
    if( !login ){
        alert("Введите имя пользователя");
        return false;
    }
    passwd = $('#login_form #id_passwd').val();
    if( !passwd ){
        alert("Введите пароль");
        return false;
    }

    $.post( "/auth/login",
            {     login: login,
                  passwd: passwd,
                  retpath: $('#login_form #id_retpath').val() || ''
             },
              function(json){
                  if(json.success){
                    if( event.data.callback ){
                    	logged_in = true;
                        event.data.callback();
                        $('#login_popup').togglePopup();
                    }else{
                        window.location = json.retpath;
                    }
                  }
                  if(json.error){
                     alert(json.error)
                  }
                  return false;
               },
             "json"
    );

    return false;
}

function submitRegForm(event){
    login = $('#registration_form #id_name').val();
    password1 = $('#registration_form #id_password1').val();
    password2 = $('#registration_form #id_password2').val();
    if( password1 && password1 != password2 ){
        alert("Пароли отличаются");
        return false;
    }

    $.post( "/auth/registration",
            { name: login,
                  email: $('#registration_form #id_email').val() || '',
                  password1: password1, password2: password2,
                  retpath: $('#registration_form #id_retpath').val() || ''
             },
              function(json){
                  if(json.success){
                    if( event.data.callback ){
                    	logged_in = true;
                        event.data.callback();
                        $('#login_popup').togglePopup();
                    }else{
                        window.location = json.retpath;
                    }
                  }
                  if(json.error){
                     alert(json.error)
                  }
                  return false;
               },
             "json"
    );

    return false;
}

function cut_anchor(url){
    // Отрезает # и все что за ней
    url = String(url);
    pos = url.indexOf('#');
    if( pos >= 0){
        return url.substr(0, pos);
    }else{
        return url;
    }
}

function init(){
	commentform = $('#commentform');
	if (commentform.length){
	    $("#commentform_link")
	        .show()
	        .click( function(){
	            $("#commentform").show();
	            $(this).hide();
	            return false;
	        });

		if( commentform.metadata().show ){
			$("#commentform_link").hide();
		}else{
			commentform.hide();
		}
		commentform
	        .bind("submit", function(){
	            post = $(this).metadata().post;
	            klass = $(this).metadata().klass;
	            if( logged_in ){
	                addComment(post, klass, "")
	            }else{
	                showLoginForm(null, '', function(){
	                    addComment(post, klass, "");
	                    window.location = window.location;
	                });
	            }
	            return false;
	        });
	}

    if( ! logged_in ){
        $('#login-link').bind("click", {retpath: '/', form: 'login'}, showLoginForm);
        $('#registration-link').bind("click", {retpath: '/'}, showLoginForm);
        $('#top_menu_new').bind("click", {retpath: '/post/new'}, showLoginForm);

        $('.js-login_required').each(function(){
        	retpath = $(this).metadata().retpath;
        	$(this).bind("click", {retpath: retpath}, showLoginForm);
        });
    }

    $('.js-vote').click( function(){
        post = $(this).metadata().post;
        klass = $(this).metadata().klass;
        if( logged_in ){
            addPostVotes(post, klass, 1);
        }else{
            retpath = "/votes/add_post_vote?post=" + post + "&klass=" + klass
                        + "&vote=1&retpath=" + escape(cut_anchor(document.location) + "#" + post)
            showLoginForm(null, retpath);
        }
        return false;
    });

    $('.js-commentlink').click( function(){
        $('.js-commentform').hide();
        $('.js-commentlink').show();
        $(this).hide();
        $('#commentform' + $(this).metadata().comment).show();
        return false;
    });

    $('.js-commentform').bind("submit", function(){
        data = $(this).metadata();
        if( logged_in ){
            addComment(data.post, data.klass, data.comment)
        }else{
            showLoginForm(null, '', function(){
                addComment(data.post, data.klass, data.comment);
                window.location = window.location;
            });
        }
        return false;
    });

    $('.js-comment-vote').click( function(){
        comment = $(this).metadata().comment;
        if( logged_in ){
            addCommentVote(comment, 1);
        }else{
            retpath = "/ajax/add_comment_vote?comment=" + comment
                        + "&vote=1&retpath=" + escape(cut_anchor(document.location) + "#c" + comment)
            showLoginForm(null, retpath);
        }
        return false;
    });

    $('.js-best_answer').click(function(){
        data = $(this).metadata();
        setBestAnswer(data.comment)
        return false;
    });

    $('.js-del_best_answer').click(function(){
        data = $(this).metadata();
        delBestAnswer(data.comment)
        return false;
    });

    $('#set_name_form').submit(function(){ return set_name(); });
    $('#set_news_form').submit(function(){ return set_news(); });

    document.documentElement.id = "js";
};

function showLoginForm(event, retpath, callback){
    if( event ){
        retpath = event.data.retpath;
        form = event.data.form;
    }else{
        form = 'registration';
    }

    $('#login_form #id_retpath').val(retpath);
    $('#registration_form #id_retpath').val(retpath);

    if( form == 'login' ){
        $('#login_form_block').removeClass('g-hidden');
        $('#registration_form_block').addClass('g-hidden');
    }else{
        $('#login_form_block').addClass('g-hidden');
        $('#registration_form_block').removeClass('g-hidden');
    }

    $('#login_popup').togglePopup();

    $('#login_form').bind("submit", {'callback':callback}, submitLoginForm);
    $('#registration_form').bind("submit", {'callback':callback}, submitRegForm);

    return false;
}

function checkCategories(event){
    if( event.target.id == 'id_categories_8' ){
        $('.categories').attr('checked', '');
        $('#id_categories_8').attr('checked', 'checked');
    }else{
        $('#id_categories_8').attr('checked', '');
    }
}

function filter_people(filter){
	$('#people_list li.js-people-li').each(function(){
		li = $(this);
		data = li.metadata();
		if( !filter || data[filter] == "True" ){
			li.show();
		}else{
			li.hide();
		}
	});
}

function selectionStart(elem){
    if (typeof this.textarea.selectionStart != "undefined"){
        //mozilla
        return this.textarea.selectionStart;
    }else{
        //ie
        var r = document.selection.createRange();
        return r.start;
    }
}

function selectionEnd(elem){
    if (typeof this.textarea.selectionEnd != "undefined"){
        //mozilla
        return this.textarea.selectionEnd;
    }else{
        //ie
        var r = document.selection.createRange();
        return r.end;
    }
}

function getSlices(elem){
    var start = selectionStart(elem);
    var end = selectionEnd(elem);
    var text = elem.value;
    //Все делится на 3 части - начало, середина и конец.
    var begin = text.slice(0,start);
    var middle = text.slice(start,end);
    var end = text.slice(end);
    return [begin, middle, end];
}

function initPostPictures(){
    textarea = $('#id_content').get(0);
    $(".js-post-picture-prepare").each( function(){
        $(this)
            .removeClass("js-post-picture-prepare")
            .click( function(){
                data = $(this).metadata()
                slices = getSlices(textarea);
                var img = "";
                if( data.method == 'normal' ){
                    img = '<glader pic="'+ data.picture +'">';
                }
                if(data.method == 'float_right'){
                    img = '<div class="float_right"><glader pic="'+ data.picture +'"></div>';
                }
                if(data.method == 'float_left'){
                    img = '<div class="float_left"><glader pic="'+ data.picture +'"></div>';
                }
                textarea.value = slices[0] + img + slices[1] + slices[2];
                return false;
            });
    });
}

function initPostButtons(){
// Навешивает действия на кнопки у редактирования поста
    textarea = $('#id_content').get(0);
    $('#btn-strong').click( function(){
        slices = getSlices(textarea);
        textarea.value = slices[0] + '<strong>' + slices[1] + '</strong>' + slices[2];
    });

    $('#btn-em').click( function(){
        slices = getSlices(textarea);
        textarea.value = slices[0] + '<em>' + slices[1] + '</em>' + slices[2];
    });

    $('#btn-ins').click( function(){
        slices = getSlices(textarea);
        textarea.value = slices[0] + '<u>' + slices[1] + '</u>' + slices[2];
    });

    $('#btn-h1').click( function(){
        slices = getSlices(textarea);
        textarea.value = slices[0] + '\n=' + slices[1] + '\n' + slices[2];
    });

    $('#btn-h2').click( function(){
        slices = getSlices(textarea);
        textarea.value = slices[0] + '\n==' + slices[1] + '\n' + slices[2];
    });

    $('#btn-link').click( function(){
        slices = getSlices(textarea);
        var url = prompt('Url страницы');
        textarea.value = slices[0] + '<a href="' + url + '">' + slices[1] + '</a>' + slices[2];
    });

    $('#btn-img').click( function(){
        slices = getSlices(textarea);
        var url = prompt('Url картинки');
        textarea.value = slices[0] + '<img src="' + url + '" alt="" />' + slices[1] + slices[2];
    });

    $('#btn-youtube').click( function(){
        slices = getSlices(textarea);
        var url = prompt('Url страницы с видеороликом');
        textarea.value = slices[0] + '<youtube>' + url + '</youtube>' + slices[1] + slices[2];
    });

    $('#btn-cut').click( function(){
        slices = getSlices(textarea);
        textarea.value = slices[0] + '<cut>' + slices[1] + slices[2];
    });

    $('#id_deferred_date').datepick({dateFormat: 'yy-mm-dd'});
    $('.categories').bind("click", checkCategories);
}

// Навешивает на все ссылки, требующие регистрации, попап с формой регистрации
$(document).ready( init );
