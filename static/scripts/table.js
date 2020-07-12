const $tableButtons = $('button');

$tableButtons.on('click', function(evt){
    let target = $(`${evt.target.attributes[4].value}`);
    if(target.is(":visible")){
        target.toggle();
    }
    else{
        target.show();
    }
});
