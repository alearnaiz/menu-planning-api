$(function() {
    $("#create-lunch").click(function() {

        var data = {
            name: getValueOrNull($("#name").val()),
            url: getValueOrNull($("#url").val()),
            days: getValueOrNull($("#days").val()),
            related_dinner_id: getValueOrNull($("#dinner").val()),
            need_starter: $("#starter").prop('checked')
        };

        $.ajax({
            method: "POST",
            url: "/web/create-lunch",
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