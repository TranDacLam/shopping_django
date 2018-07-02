jQuery(document).ready(function($) {
    $('#form-language select').change(function(){
        $('#form-language').submit();
    });
});