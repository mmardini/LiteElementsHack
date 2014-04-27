var initial_networks = function(json_str) {
    var json_obj = jQuery.parseJSON(json_str.replace(/&quot;/g,"\""));
    render_json(json_obj);
    setTimeout(update_networks, 5000);
};

function update_networks() {
    $.ajax({
        dataType: "json",
        url: "json/wifi",
        success: function (json_obj) {
            render_json(json_obj);
        },
        complete: function() {
            /*  For a short interval (5 seconds in this situation),
                setTimeout() is better than setInterval(), because using 
                setTimeout() in the following way will make sure the first
                request is completed before making another request.
            */
            setTimeout(update_networks,5000);
        }
    });
}

function render_json(json_obj) {
    if (json_obj.networks.length > 0) {
        $('#info').html(json_obj.networks.join("<br/>"));
    }
}