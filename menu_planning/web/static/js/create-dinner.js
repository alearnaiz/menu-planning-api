$(function() {
    $("#create-dinner").click(function() {

        var data = {
            name: getValueOrNull($("#name").val()),
            url: getValueOrNull($("#url").val()),
            days: getValueOrNull($("#days").val())
        };

        $.ajax({
            method: "POST",
            url: "/web/create-dinner",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json"
        }).done(function(food) {
            window.location.href = "/web/food/"+food.id+"/ingredients"
        }).fail(function() {
            $("#error-panel").removeClass("hidden");
        });
    });
});