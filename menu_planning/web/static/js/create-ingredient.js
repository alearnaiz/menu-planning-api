$(function() {

    $("#create-ingredient").click(function() {

        var data = {
            name: getValueOrNull($("#name").val())
        };

        $.ajax({
            method: "POST",
            url: "/web/ingredient",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json"
        }).done(function() {
            window.location.href = "/web/ingredients";
        }).fail(function() {
            $("#error-panel").removeClass("hidden");
        });
    });
});