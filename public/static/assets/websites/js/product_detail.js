$(document).ready(function(){

    // Quantity product
    $('.minusQuantity').on('click', function(){
        var quantity = parseInt($('#quantity').val());
        if(quantity > 1){
            $('#quantity').val(quantity - 1);
        }
    });

    $('.plusQuantity').on('click', function(){
        var quantity = parseInt($('#quantity').val());
        $('#quantity').val(quantity + 1);
    });


    // Comment
    $('.reply-btn').on('click', function(){
        var comment_id = $(this).attr('data-id-comment');
        $('#Reply-customer form .comment-parrent').val(comment_id);
    });


    var init_rate = parseInt($('#init-rate').attr('data-init-rate'));
    var product_id = parseInt($('#init-rate').attr('data-product-id'));

    $('#rating_product').barrating({
        theme: 'fontawesome-stars',
        initialRating: init_rate,
        onSelect: function(value, text, event) {
            if (typeof(event) !== 'undefined') {
                var select_rate = parseInt(value);

                $.ajax({
                    url: '/vi/product/rating/',
                    type: 'POST',
                    data: {
                        'product_id': product_id,
                        'point': select_rate
                    },
                    context: this,
                })
                .done(function(response) {
                    $('#rating_product').barrating('set', response.point);
                    toastr.success(response.message);
                })
                .fail(function(error) {
                    if(error.status == 500){
                        toastr.error(error.statusText);
                    }else{
                        toastr.error(error.responseJSON.message);
                    }
                });
            }
        }
    });
});