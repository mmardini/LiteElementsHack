var initial_battery = function(json_str) {
    var json_obj = jQuery.parseJSON(json_str.replace(/&quot;/g,"\""));
    render_json(json_obj);
    // Calls update_battery() every 2 minutes.
    setInterval(update_battery, 120000); 
};

function update_battery() {
    $.ajax({
        dataType: "json",
        url: "json/battery",
        success: function (json_obj) {
            render_json(json_obj);
        },
    });
}

function render_json(json_obj) {
    $('#battery-status').text(json_obj.status);
    $('#battery-percent').text(json_obj.percent);
    $('#battery-time').text(json_obj.time);
    $('#battery-time-info').text(json_obj.time_info);
    $('#battery-bar').css({"width": json_obj.percent});
}