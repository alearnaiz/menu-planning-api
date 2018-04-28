$(function() {

    $("#send-foods").click(function() {

        var menuId = $("#menu-id").val();

        var foods = $(".food:checked");

        var data = $.map(foods, function(el) {
            return {
                id: el.value
            };
        });

        $.ajax({
            method: "POST",
            url: "/web/send-foods-to-grocery-list/"+menuId,
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json"
        }).done(function() {
            window.location.href = "/web/grocery-list";
        }).fail(function() {
            $("#error-panel").removeClass("hidden");
        });
    });
});