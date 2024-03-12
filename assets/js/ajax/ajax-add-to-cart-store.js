function add_to_cart(id) {
    $.get(`/cart/add-to-cart-store/${id}/`).then(response => {
        if (response.bool === true) {
            $("#home_cart_list").html(response.data)
        }
    })
}