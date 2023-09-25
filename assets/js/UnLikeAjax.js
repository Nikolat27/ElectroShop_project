
$('#unlike-form-ajax').submit(function (e) {
    e.preventDefault();
    let like_count = document.getElementById("liked-products")

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: 'json',

        beforeSend: function () {
            console.log("Unliking product...");
        },
        success: function (response) {
            console.log("Product Unliked successfully!");
            ``
            if (response.bool === true) {
                $("#product-div").html(response.data)
                like_count.innerText = response.likedproducts
            }
        }
    })
})