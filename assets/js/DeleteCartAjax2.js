$('#delete-product-form').submit(function (e) {
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: 'json',

        beforeSend: function () {
            console.log("Deleting Product...");
        },
        success: function (response) {
            console.log("Product Deleted!");
            if (response.bool === true) {
                $("#cart-items-count").text(response.totalcartitems)
                $("#cart-div").html(response.data)
            }
        }
    })
})