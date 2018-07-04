$(document).ready(function() {
    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('.scrollToTop').fadeIn();
        } else {
            $('.scrollToTop').fadeOut();
        }
    });

    //Click event to scroll to top
    $('.scrollToTop').click(function(){
        $('html, body').animate({scrollTop : 0},800);
        return false;
    });

    // $(".dropdown").hover(            
    //     function() {
    //         $('.dropdown-menu', this).not('.in .dropdown-menu').stop(true,true).slideDown("400");
    //         $(this).toggleClass('open');        
    //     },
    //     function() {
    //         $('.dropdown-menu', this).not('.in .dropdown-menu').stop(true,true).slideUp("400");
    //         $(this).toggleClass('open');       
    //     }
    // );

    $('.nav .mega-dropdown').mouseenter(function() {
        $(this).children('.mega-dropdown-menu').stop().slideDown('400')
    }).mouseleave(function() {
        $(this).children('.mega-dropdown-menu').stop().slideUp('400')
    });

    jQuery(document).on('click', '.mega-dropdown', function(e) {
        e.stopPropagation()
    })
});