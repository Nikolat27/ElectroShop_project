function delete_from_cart(id) {
    $.get(`/cart/remove-from-cart/${id}/`).then(response => {
        if (response.bool === true) {
            $("#home_cart_list").html(response.data)
        }
    })
}
