function update_cart(id) {
    let quantity = document.getElementById(`${id}-quantity`).value
    let new_price = document.getElementById(`${id}-total-price`)
    let subtotal = document.getElementById(`subtotal-price`)
    console.log(quantity)

    $.ajax({
        url: `/cart/update/${id}`,
        data: {
            new_quantity: quantity
        },
        dataType: 'json',

        success: function (response) {
            if (response.bool === true) {
                new_price.innerText = `$${response.new_price}`
                subtotal.innerText = `$${response.subtotal}`
            } else {
                console.log("Error!")
            }
        }
    });

}
