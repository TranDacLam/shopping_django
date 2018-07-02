$(document).ready(function() {
    $('.flexbox-grid-default').on('click', function(){
        var value = $(this).closest('.group-collection').attr('aria-expanded');
        if(value == 'true'){
            $(this).closest('.group-collection').attr('aria-expanded', 'false');
        }else{
            $(this).closest('.group-collection').attr('aria-expanded', 'true');
        }
    });
});