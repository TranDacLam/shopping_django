$(document).ready(function(){

    // Zoom image
    $(".product-image-feature").elevateZoom({scrollZoom : true});


    if($(".product-thumb-vertical").length > 0 && $(window).width() >= 768 ) {
        $(".product-thumb-vertical").mThumbnailScroller({
            axis:"y",
            type:"click-thumb",
            theme:"buttons-out",
            type:"hover-precise",
            contentTouchScroll: true
        });
        setTimeout(function(){
            $('.product-thumb-vertical').css('height',$('.product-image-feature').height());
            $('#sliderproduct').show();
        },500);
    }
    if($(".product-thumb-vertical").length > 0 && $(window).width() < 767 ) {
        $(".product-thumb-vertical").mThumbnailScroller({
            axis:"x",
            theme:"buttons-out",
            contentTouchScroll: true
        });
        $('#sliderproduct').show();
    }


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

    // change image
    $('.mTSThumbContainer').on('click', function(){
        $(".mTSThumbContainer a").removeClass('zoomGalleryActive');
        $(this).find('a').addClass('zoomGalleryActive');
        var url_image = $(this).find('a').attr('data-image');
        var zoomImage = $(".product-image-feature");
        $('.zoomContainer').remove();
        zoomImage.removeData('elevateZoom');
        // Update source for images
        zoomImage.attr('src', url_image);
        zoomImage.data('zoom-image', url_image);
        // Reinitialize EZ
        zoomImage.elevateZoom({scrollZoom : true});
    });


    // Comment
    $('.reply-btn').on('click', function(){
        var comment_id = $(this).attr('data-id-comment');
        $('#Reply-customer form .comment-parrent').val(comment_id);
    });
});