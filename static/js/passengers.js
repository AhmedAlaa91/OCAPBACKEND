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

    set_status_class();

});

function set_status_class(){
    const status_items = document.getElementsByName("passenger_status");
    for(item in status_items){
        element = status_items[item]
        class_name = element.textContent.toLowerCase();
        element.className += class_name;
    }
}

function show_confirmation_dialog(title,message,action){
    modal = $('#confirmation_modal')
    modal.modal('show')
    modal.find('.modal-title').text(title)
    modal.find('.modal-body').text(message)
    if(action == "accept"){
        document.getElementById("modal-btn-confirm").onclick = accept
    }
    else if(action == "reject"){
        document.getElementById("modal-btn-confirm").onclick = reject
    }
    else if(action == "cancel"){
        document.getElementById("modal-btn-confirm").onclick = cancel
    }
    else{
        document.getElementById("modal-btn-confirm").onclick = function(){$('.modal').modal('hide'); alert(action)}}

    $('#confirm').show()
}

function accept() {
    $('.modal').modal('hide');
    input_data = {"ride_id" : 1, "passenger_id" : 1}
    $.ajax({
        type: 'POST',
        url: "/ride/passengers/accept",
        dataType: 'json',
        data:input_data,
        success: function (result) {
            window.location.href = window.location
        },
        error: function(error){
            window.location.href = window.location
            console.log(error)
        }
    });
}

function reject() {
    $('.modal').modal('hide');
    input_data = {"ride_id" : 1, "passenger_id" : 1}
    $.ajax({
        type: 'POST',
        url: "/ride/passengers/reject",
        dataType: 'json',
        data:input_data,
        success: function (result) {
            window.location.href = window.location
        },
        error: function(error){
            window.location.href = window.location
            console.log(error)
        }
    });
}

function cancel() {
    $('.modal').modal('hide');
    input_data = {"ride_id" : 1, "passenger_id" : 1}
    $.ajax({
        type: 'POST',
        url: "/ride/passengers/cancel",
        dataType: 'json',
        data:input_data,
        success: function (result) {
            window.location.href = window.location
        },
        error: function(error){
            window.location.href = window.location
            console.log(error)
        }
    });
}