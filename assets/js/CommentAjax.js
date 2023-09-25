function set_value(id) {
    console.log(id);
    setTimeout(() => document.getElementById('parent_id').value = id, 0);
}

function submitReply(event, form, id) {
    console.log("hello world2!")
    event.preventDefault()
    const formData = new FormData(form)
    formData.append("product_id", id)
    const urlEncoded = new URLSearchParams(formData).toString()
    $.ajax({
        type: 'POST',
        url: `http://127.0.0.1:8000/products/ajax-add-review/${id}`,
        // processData: false,
        data: urlEncoded,
        success: (res) => {
            if (res.bool) {
                removeForm(form)
                $('#comment_part2').html(res.comment_part1)
            }
        }
    })
}

$('#commentForm').submit(function (e) {
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),

        dataType: "json",

        success: function (response) {
            console.log("Comment Saved!");

            if (response.bool === true) {
                $('#review-res').html("Review Added Successfully!")
                $('#comment_part1').html(response.comment_part2)
                $('#comment_part2').html(response.comment_part1)
            }
        }
    })
})




