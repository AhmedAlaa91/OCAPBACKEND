
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



function set_status_class(){
    
    const status_items = document.getElementsByName("passenger_status");

    for(item in status_items){
        element = status_items[item]
        class_name = element.innerText.toLowerCase();
        element.className += class_name;
    }
}

$(document).ready(function() {

   // set_status_class();
   
   
   
   });

async function show_confirmation_dialog(title,message,action,ride,requestor){



    modal = $('#confirmation_modal')
    modal.modal('show')
    modal.find('.modal-title').text(title)
    modal.find('.modal-body').text(message)
    if(action == "accept"){
       // document.getElementById("modal-btn-confirm").onclick = hidemodal
      // modal.find('.reason').hide();
      modal.find('#reasonl').hide();
       modal.find('#reason').hide();
       await hidemodal();
        accept(ride,requestor) ;
    }
    else if(action == "reject"){
       // document.getElementById("modal-btn-confirm").onclick = reject
       modal.find('#reasonl').show();
       modal.find('#reason').show();

       var textarea = document.querySelector("#reason");
     
        var commenttxt="";
        this.lastKey= "";
        textarea.addEventListener("input", (e) => {
            this.commenttxt= e.target.value;
           
         });
      
         await hidemodal();
         this.commenttxt=textarea.value
     
      
        reject(ride,requestor,this.commenttxt) ;
    }
    else if(action == "cancel"){
       // document.getElementById("modal-btn-confirm").onclick = cancel
       modal.find('#reasonl').show();
       modal.find('#reason').show();


       var textarea = document.querySelector("#reason");
     
       var commenttxt="";
       this.lastKey= "";
       textarea.addEventListener("input", (e) => {
           this.commenttxt= e.target.value;
          
        });
      
        await hidemodal();
        this.commenttxt=textarea.value
 
       
        cancel(ride,requestor,this.commenttxt) ;
    }
    else{
        document.getElementById("modal-btn-confirm").onclick = function(){$('.modal').modal('hide'); alert(action)}}

    $('#confirm').show()
}



function hidemodal() {


    return new Promise(resolve => 
        $('#modal-btn-confirm').on('click', () => {
            $('.modal').modal('hide');
            resolve();
            }
        )
    );
}

async function accept(rideid,requestorid)  {

   
    

    let csrftoken= document.querySelector('input[name="csrfmiddlewaretoken"]').value
    
    $.ajaxSetup({
    
    beforeSend: function(xhr, settings) {
    
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
    
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    
      }
    
    }
    
    });

    
     $.ajax({
    
      url: "/ride/passengers",
      
      headers:{ Accept : "application/json",         
      "Content-Type": "application/json" ,
      'csrfmiddlewaretoken' : csrftoken },
      type: "POST",
     
    
      
      accept:"application/json",
      data :JSON.stringify( { "RideRequested_id": rideid,
              
              "Requestor_id": requestorid,
              "comment" : ' ',
              "status": "Accepted"}),
      contentType: "application/json",
      success: function()
      {
            // it will update the html of table body
          $("#passengers_form").load(location.href + " #passengers_form");
         
          
      }
    });

    }



async function reject(rideid,requestorid,commenttxt)  {

   
 

        let csrftoken= document.querySelector('input[name="csrfmiddlewaretoken"]').value
    
        $.ajaxSetup({
        
        beforeSend: function(xhr, settings) {
        
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        
              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        
          }
        
        }
        
        });
    
        
    

    $.ajax({
        url: "/ride/passengers",
    
        headers:{ Accept : "application/json",         
        "Content-Type": "application/json" ,
        'csrfmiddlewaretoken' : csrftoken },
        type: "POST",
       
    
        
        accept:"application/json",
        data :JSON.stringify( { "RideRequested_id": rideid,
                
                "Requestor_id": requestorid,
                "comment": commenttxt ,
                "status": "Rejected"
                }),
        contentType: "application/json",
        success: function(response)
        {
              // it will update the html of table body
            $("#passengers_form").load(location.href + " #passengers_form");
            
              //  document.addEventListener("DOMContentLoaded", set_status_class());
            
            
   


        }
    });
    
}



async function cancel(rideid,requestorid,commenttxt)  {

   




    let csrftoken= document.querySelector('input[name="csrfmiddlewaretoken"]').value
    
    $.ajaxSetup({
    
    beforeSend: function(xhr, settings) {
    
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
    
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    
      }
    
    }
    
    });

    
     $.ajax({
    
      url: "/ride/passengers",
      
      headers:{ Accept : "application/json",         
      "Content-Type": "application/json" ,
      'csrfmiddlewaretoken' : csrftoken },
      type: "POST",
     
    
      
      accept:"application/json",
      data :JSON.stringify( { "RideRequested_id": rideid,
              
              "Requestor_id": requestorid,
              "comment": commenttxt ,
              "status": "Cancelled"}),
      contentType: "application/json",
      success: function()
      {
            // it will update the html of table body
          $("#passengers_form").load(location.href + " #passengers_form");
      }
    });
    
    }