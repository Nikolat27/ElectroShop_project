$('#update-cart-form').submit(function (e) {
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: 'json',

        beforeSend: function () {
            console.log("Updating Product...");
        },
        success: function (response) {
            console.log("Product Updated!");``
            if (response.bool === true) {
                $("#cart-items-count").text(response.totalcartitems)
                $("#cart-div").html(response.data)
            }
        }
    })
})