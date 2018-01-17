$(function() {

    $("#edit-menu").click(function() {

        var menuId = $("#menu-id").val();

        var data = {
            favourite: $("#favourite").prop('checked'),
            name: getValueOrNull($("#name").val()),
            daily_menus: []
        };

        var dailyMenus = $(".daily-menu");

        for (var i = 0; i < dailyMenus.length; i++) {
            var dailyMenu = dailyMenus[i];
            var id = $(dailyMenu).data("id");
            var starterId = $(dailyMenu).find(".starter option:selected").val();
            var lunchId = $(dailyMenu).find(".lunch option:selected").val();
            var dinnerId = $(dailyMenu).find(".dinner option:selected").val();

            var starter = null;
            if (isNotEmpty(starterId)) {
                starter = {
                    id: starterId
                };
            }

            var lunch = null;
            if (isNotEmpty(lunchId)) {
                lunch = {
                    id: lunchId
                };
            }

            var dinner = null;
            if (isNotEmpty(dinnerId)) {
                dinner = {
                    id: dinnerId
                };
            }

            data.daily_menus.push({
                id: id,
                starter: starter,
                lunch: lunch,
                dinner: dinner
            });
        }

        $.ajax({
            method: "PUT",
            url: "/web/edit-menu/"+menuId,
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json"
        }).done(function() {
            window.location.href = "/web/menu/"+menuId;
        }).fail(function() {
            $("#error-panel").removeClass("hidden");
        });
    });
});