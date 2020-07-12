const $editForm = $('#edit-form');
const $editButton = $('#edit-button');
const $imagefield1 = $('#image');
const $imagefield2 = $('#image1');
const $imagefield3 = $('#image2');
const $imagefield4 = $('#image3');
const $changeimage = $('#changeimage');
const $changeimage1 = $('#changeimage1');
const $changeimage2 = $('#changeimage2');
const $changeimage3 = $('#changeimage3');
let changeimagesChecked = false;

$(document).ready(function(evt){
    if($changeimage.prop('checked')==true){
        $imagefield1.prop('disabled', false);
    }
    if($changeimage1.prop('checked')==true){
        $imagefield2.prop('disabled', false);
    }
    if($changeimage2.prop('checked')==true){
        $imagefield3.prop('disabled', false);
    }
    if($changeimage3.prop('checked')==true){
        $imagefield4.prop('disabled', false);
    }
    
})

$editForm.toggle();

$editButton.on('click', function(evt){
    if($editForm.is(":visible")){
        $editForm.toggle();
        $editButton.text('Show Edit Product Form');
    }
    else{
        $editForm.show();
        $editButton.text('Hide Edit Product Form');
    }
})

$changeimage.on('click', function(evt){
    if($changeimage.prop('checked')== true){
        $imagefield1.prop('disabled', false);
    }
    else{
        $imagefield1.prop('disabled', true);
    }
    
})
$changeimage1.on('click', function(evt){
    if($changeimage1.prop('checked')== true){
        $imagefield2.prop('disabled', false);
    }
    else{
        $imagefield2.prop('disabled', true);
    }
    
})
$changeimage2.on('click', function(evt){
    if($changeimage2.prop('checked')== true){
        $imagefield3.prop('disabled', false);
    }
    else{
        $imagefield3.prop('disabled', true);
    }
    
})
$changeimage3.on('click', function(evt){
    if($changeimage3.prop('checked')== true){
        $imagefield4.prop('disabled', false);
    }
    else{
        $imagefield4.prop('disabled', true);
    }
    
})