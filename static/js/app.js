// AJAX for posting
function receiveSubmit() {
    console.log("submit is working!") // sanity check
    $.ajax({
        url : "/submit", // the endpoint
        type : "POST", // http method
        data : { request : $('#file-submit-form').val() }, // data sent with the post request FILES DATA

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            //<!-- timing["q_time"], timing["tree_load_time"], timing["nn_time"], timing["cc_time] -->

            if (json.status.uploadStatus) {

                $("#updates-timing").append("<li> Job queued in "+json.timing.q_time+" seconds </li>");
                $("#updates-timing").append("<li> Search tree loeaded in "+json.timing.tree_load_time+" seconds </li>");
                $("#updates-timing").append("<li> Nearest neighbor search completed in "+json.timing.nn_time+" seconds </li>");
                $("#updates-timing").append("<li> Colores search completed in "+json.timing.cc_time+" seconds </li>");

                $("#link-button").html("<a href='/results/"+json.status.jobid+"' class='button'>take me to my blob</a>");
            } else {
                $("#error-message").html("<p>"+json.status.errorMsg+"</p>")
            }

            /* 
            $("#talk").prepend("<li><strong>"+json.text+"</strong> - <em> "+json.author+"</em> - <span> "+json.created+"</span></li>"); */
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#error-message').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};