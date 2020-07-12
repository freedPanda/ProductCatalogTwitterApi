const $addForm = $('#add-form');
const $addButton = $('#add-button');

//$(document).ready(function(evt){
    //$addForm.toggle();
//});

$addButton.on('click', function(evt){
    if($addForm.is(":visible")){
        $addForm.toggle();
        $addButton.text('Show Add Product Form');
    }
    else{
        $addForm.show();
        $addButton.text('Hide Add Product Form');
    }
})