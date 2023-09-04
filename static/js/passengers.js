function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

$(document).ready(function() {
   
});

async function show_confirmation_dialog(title,message,action,ride,requestor){

    modal = $('#confirmation_modal')
    modal.modal('show')
    modal.find('.modal-title').text(title)
    modal.find('.modal-body').text(message)
    var passenger_response_reason="";
    if(action == "accept"){
        modal.find('#reasonl').hide();
        modal.find('#reason').hide();
        await hide_modal();
        response_to_passenger_request(ride,requestor,"2","");
    }
    else if(action == "reject"){
        modal.find('#reasonl').show();
        modal.find('#reason').show();
        var textarea = document.querySelector("#reason");
        this.lastKey= "";
        textarea.addEventListener("input", (e) => {
            this.passenger_response_reason= e.target.value;
        });
        await hide_modal();
        this.passenger_response_reason = textarea.value
        response_to_passenger_request(ride,requestor,"3",this.passenger_response_reason);
    }
    else if(action == "cancel"){
       modal.find('#reasonl').show();
       modal.find('#reason').show();
       var textarea = document.querySelector("#reason");
       this.lastKey= "";
       textarea.addEventListener("input", (e) => {
           this.passenger_response_reason= e.target.value;
       });
       await hide_modal();
       this.passenger_response_reason=textarea.value
       response_to_passenger_request(ride,requestor,"4",this.passenger_response_reason)
    }
    else {
        document.getElementById("modal-btn-confirm").onclick = function(){$('.modal').modal('hide'); alert(action)}
    }
    $('#confirm').show()
}

async function response_to_passenger_request(ride_id,requestor_id,passenger_response_code,comment){
    let csrftoken= document.querySelector('input[name="csrfmiddlewaretoken"]').value
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
      $("#avatarpic"+requestor_id).hide();
      $("#loader"+requestor_id).show();
    }
    });

    $.ajax({
        url: "/ride/passengers",
        headers:{
                    Accept : "application/json",
                    "Content-Type": "application/json" ,
                    'csrfmiddlewaretoken' : csrftoken
                 },
        type: "POST",
        accept:"application/json",
        data :JSON.stringify( { "RideRequested_id": ride_id,"Requestor_id": requestor_id,"comment": comment ,"status": passenger_response_code}),
        contentType: "application/json",
        success: function() {
            $("#avatarpic"+requestor_id).show();
            $("#loader"+requestor_id).hide();
            // it will update the html of table body
            $("#passengers_form").load(location.href + " #passengers_form");
        },
        error: function (error) {
            $("#avatarpic"+requestor_id).show();
            $("#loader"+requestor_id).hide();
            console.log(error);
        }
    });
}

function hide_modal() {

    return new Promise(resolve =>
        $('#modal-btn-confirm').on('click', () => {
            $('.modal').modal('hide');
            resolve();
            }
        )
    );
}