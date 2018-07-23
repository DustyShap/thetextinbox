$(document).ready(function(){
  var socket = io.connect(location.protocol + '//' + document.domain + ":" + location.port);
  var $new_user_message = $("#message_container_template").clone()
  var $new_searched_contact_template =  $("#contact_container_template").clone()

  $(document).on("click",'#all_users_button_container',function(event){
    window.location.href = "/"
  })



  $("#user_search").keypress(function(event){
    if (event.keyCode == 13){
      searchUser()
    }
  })
  $(document).on("click","#user_search_button",function(event){
      searchUser()
  })

  $(document).on("click",".contact_container",function(event){
    $("#all_users_button_container").css('background-color','#ffffff')
    $('.contact_container').css('background-color','#ffffff');
    $(".message_information").css('background-color','#ffffff');
    var $user_id_clicked = $(this).children(".message_information").attr('id')
    $(this).css('background-color','#d6d6d6');
    $(this).children(".message_information").css('background-color','#d6d6d6');
    $("#message_container").empty()
    $.ajax({
      data:{
        user_id_clicked: $user_id_clicked
      },
      type:'POST',
      url:'/all_single_user_messages'
    })
    .done(function(data){
      for (var i = 0; i < data.length; i++){
        var $new_msg = $new_user_message.clone()
        $new_msg.removeAttr('id')
        $new_msg.children('.message_display_name').html(data[i].user)
        $new_msg.children('.message_from_number').html(data[i].number)
        $new_msg.children('.message_body_container').html(data[i].msg_body)
        $new_msg.children('.message_received_time').html(data[i].timestamp)
        if (data[i].message_media_url){
          $new_msg.addClass('message_with_picture')
          $new_msg.children("#media_placeholder").addClass('message_media_container').removeAttr('id')
          $new_msg.children('.message_media_container').append('<img class="text_image" src='+data[i].message_media_url+'/>')
        }
        $new_msg.appendTo("#message_container").css('display','flex')

      }
    })
  })

  $(document).on("click",".edit_name",function(event){
    $new_div = $(this).parent(".message_username").parent();
    var previousValue = $(this).parent(".message_username").text().trim()
    var $input = "<input value='"+previousValue+"' class='name_change' maxlength='22'/>"
    var $name_change_button = $("<button>Update</button>").attr('id','name_change_button')
    $(this).parent(".message_username").replaceWith("<div class='message_username'>"+$input+"</div>")
    $new_div.children('.message_username').append($name_change_button)
  })

  $(document).on("click","#name_change_button",function(event){
    var $new_name = $(this).parent().children(".name_change").val()
    var $number_to_update = $(this).parent().parent().children('.contact_from_number').text()
    var $new_element = "<div class='message_username'>"+$new_name+"<i class='fa fa-edit edit_name'></i></div>"
    $(this).parent().replaceWith($new_element)
    $.ajax({
      data:{
        new_name:$new_name,
        number_to_update: $number_to_update
      },
      type:'POST',
      url:'/update_name'
    })
  })


  $(document).on("click", ".text_image", function(event){
    window.open($(this)[0].currentSrc)
  })



  socket.on('msg received',function(data){


    var number = data.user.phone_number;
    var message_body = data.message.message_body;
    var timestamp = data.message.timestamp;
    var display_name = data.user.display_name;
    var location = data.user.location;
    var total_texts_from_user = data.total_texts_from_user;
    var does_contact_exist = data.does_user_exist;
    var user_id = data.user.user_id;
    var media = data.message.media;



    if (does_contact_exist === true){

      var $contact_to_update = $("#"+user_id)
      $contact_to_update.parent().children(".message_user_total").html(total_texts_from_user)
      $contact_to_update.parent().children(".message_user_total").html(total_texts_from_user)
      $contact_container = $contact_to_update.parent()
      $contact_container.detach().prependTo("#sidebar_contacts");


    } else if (does_contact_exist === false) {

        var $new_contact_message_container =  $("#contact_container_template").clone()
        $new_contact_message_container.removeAttr("id")
        $new_contact_message_container.children(".message_information").attr('id',user_id)
        $new_contact_message_container.children().children(".message_username").html(display_name)
        $new_contact_message_container.children().children(".contact_from_number").html(number)
        $new_contact_message_container.children().children(".message_from_location").html(location)
        $new_contact_message_container.children(".message_user_total").html(total_texts_from_user)
        $new_contact_message_container.prependTo("#sidebar_contacts").css('display','flex')

    }

    var $new_message = $("#message_container_template").clone()
    console.log($new_message)
    $new_message.removeAttr("id")
    $new_message.children('.message_display_name').html(display_name)
    $new_message.children('.message_from_number').html(number)
    $new_message.children('.message_body_container').html(message_body)
    $new_message.children('.message_received_time').html(timestamp)


    if(media){
      $new_message.addClass('message_with_picture')
      $new_message.children("#media_placeholder").addClass('message_media_container').removeAttr('id')
      $img_url = data.message.media;
      $new_message.children('.message_media_container').append('<img class="text_image" src='+$img_url+'/>')
    }

    $new_message.prependTo("#message_container").css('display','flex')
    window.location.href = "/"

  })

  function searchUser() {
    if($("#user_search").val() == ''){
      return
    }
    $.ajax({
      data:{
        search_term:$("#user_search").val()
      },
      type:'POST',
      url:'/search_for_user'
    })
    .done(function(data){

      $("#sidebar_contacts").empty()
      for (var i = 0; i < data.length; i++){

        $new_searched_contact = $new_searched_contact_template.clone()
        $new_searched_contact.removeAttr("id")
        $new_searched_contact.children(".message_information").attr('id',data[i].user_id)
        $new_searched_contact.children().children('.message_username').prepend(data[i].user)
        $new_searched_contact.children().children('.contact_from_number').html(data[i].number)
        $new_searched_contact.children().children('.message_from_location').html(data[i].location)
        $new_searched_contact.children(".message_user_total").html(data[i].text_count)
        $new_searched_contact.appendTo("#sidebar_contacts").css('display','flex')

      }
    })
  }

});
