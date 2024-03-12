// $(document).ready(function () {
//     $("#loadMore").on("click", function () {
//         let currentProducts = $(".product-box").length;
//         let limit = $(this).attr("data-limit");
//         let total = $(this).attr("data-total");
//
//         // Start ajax
//         $.ajax({
//             url: '/products/load-more-data',
//             data: {
//                 limit: limit,
//                 offset: currentProducts
//             },
//             dataType: 'json',
//             beforeSend: function () {
//                 $("#loadMore").attr('disabled', true);
//                 $(".load-more-icon").addClass('fa-spin');
//             },
//             success: function (response) {
//                 $("#filteredProducts").append(response.data);
//                 $("#loadMore").attr('disabled', false);
//                 $(".load-more-icon").removeClass('fa-spin');
//
//                 let totalShowing = $(".product-box").length;
//                 if (totalShowing === total) {
//                     $("#loadMore").remove();
//                 }
//             }
//         });
//         // End
//     })
// })