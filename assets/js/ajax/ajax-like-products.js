function like(id, slug) {

    let element = document.getElementById(`${slug}`)
    let count = document.getElementById("like-count")
    let total = document.getElementById(`total-${slug}-likes`)

    $.get(`/products/add_like/${id}`).then(response => {
        if (response["response"] === "liked") {
            element.className = "fa fa-heart"
            count.innerText = Number(count.innerText) + 1
            total.innerText = response['total']
        } else {
            element.className = "fa fa-heart-o"
            count.innerText = Number(count.innerText) - 1
            total.innerText = response['total']
        }
    })
}
