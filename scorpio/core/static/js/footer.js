var height = $(this).height() - $(".items").height() - 170;
    footer.style.height = height + 'px'
    if(height<=0){
        footer.style.marginTop = '200px'
    }