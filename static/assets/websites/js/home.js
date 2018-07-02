jQuery(document).ready(function($) {
    $('#form-language select').change(function(){
        $('#form-language').submit();
    });

    $("#scroller").simplyScroll({
        orientation:'vertical',
        customClass:'vert'
    });

    var owl = $('.owl-carousel');
    owl.owlCarousel({
        margin: 10,
        nav: true,
        loop: true,
        dots: false,
        navText : ['<i class="fa fa-angle-left" aria-hidden="true"></i>','<i class="fa fa-angle-right" aria-hidden="true"></i>'],
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 3,
                margin: 5
            },
            1000: {
                items: 4
            }
        }
    })
});