$(function() {

    $("#edit-ingredients").click(function() {
        var foodId = $("#food-id").val();

        var data = [];

        var ingredients = $("#ingredients tr");

        for (var i = 0; i < ingredients.length; i++) {
            var ingredient = ingredients[i];
            var ingredientId = $(ingredient).find(".ingredient-id option:selected").val();
            var ingredientQuantity = $(ingredient).find(".ingredient-quantity").val();

            if (isNotEmpty(ingredientId)) {
                var ingredientData = {
                    ingredient: {
                        id: ingredientId
                    },
                    quantity: getValueOrNull(ingredientQuantity)
                };

                data.push(ingredientData);
            }

        }

        $.ajax({
            method: "PUT",
            url: "/web/food/"+foodId+"/ingredients",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json"
        }).done(function() {
            window.location.href = "/web/food/"+foodId
        }).fail(function() {
            $("#error-panel").removeClass("hidden");
        });
    });

    $("#add-ingredient").click(function() {

        $.ajax({
            method: "GET",
            url: "/web/template-ingredient",
            dataType: "html"
        }).done(function(template) {
            $("table").append(template);
        });

    });
});