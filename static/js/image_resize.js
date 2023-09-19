$(() => {
    $("#loader").hide();
    $("#preview").show();
    var csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    $("#profile_picture").on("change", function (e) {
        e.preventDefault();
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                $("#loader").show();
                $("#preview").hide();
            }
        });
        var data = new FormData($('form').get(0));
        $.ajax({
            url: '/user/profile/preview',
            type: 'POST',
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function (data) {
                $("#loader").hide();
                $("#preview").show();
                $('#preview').attr('src', `data:image;base64,${data.photo_resized}`)
            },
            error: function (error) {
                console.log(error);
            }
        });

    });


});