function like(id, slug) {
    console.log(id)
    console.log(slug)

    let element = document.getElementById(`${slug}`)
    console.log(element)

    $.get(`/products/add_like/${id}`).then(response => {
        if (response["response"] === "liked") {
            console.log("product liked")
            element.className = "fa fa-heart"
        } else {
            console.log("product unliked")
            element.className = "fa fa-heart-o"
        }
    })
}
