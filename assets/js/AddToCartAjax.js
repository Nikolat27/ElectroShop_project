$('#add-to-cart-form').submit(function (e) {
    e.preventDefault();

    let this_val = $("#add-to-cart-btn");
    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: 'json',

        beforeSend: function () {
            this_val.html("Adding to cart...")
            console.log("Adding Product to cart...");
        },
        success: function (response) {
            console.log("Product Saved!");``

            if (response.bool === true) {
                setTimeout(() => this_val.html("Product Added"), 700);
                setTimeout(() => this_val.html("ADD TO CART"), 1500);
                $("#cart-items-count").text(response.totalcartitems)
                $("#cart-view").html(response.data)
            }
        }
    })
})