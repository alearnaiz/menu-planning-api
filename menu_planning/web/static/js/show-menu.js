$(function() {

    $("#send-products").click(function() {
        var menuId = $("#menu-id").val();

        $.ajax({
            method: "GET",
            url: "/web/send-products/"+menuId,
            contentType: "application/json"
        }).done(function() {
            window.location.href = "/web/grocery-list";
        }).fail(function() {
            $("#error-panel").removeClass("hidden");
        });
    });
});