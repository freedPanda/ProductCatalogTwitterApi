const $clearButton = $('#clear-button');
const $categoryForm = $('#category-form');
const $categoryButton = $('#category-button');
const $notFound = $('#none-found');
const $plateCheckBox = $('#plate');
const $bowlCheckBox = $('#bowl');
const $trayCheckBox = $('#tray');
const $basketCheckBox = $('#basket');
const $miscCheckBox = $('#misc');
const $signCheckBox = $('#sign');
const $furnitureCheckBox = $('#furniture');
const $boxCheckBox = $('#box');
const $allRows = $('.row');
const $theRows = $('.row.mt-3');

let realRows = [];
let productList = [];
let productIdList = [];
let catList = [];
let productMap = new Map();

//productsCollected variable is used to make sure productMap
//is initialized only once
let productsCollected = false;

//this event is the main function
$categoryForm.submit(function(evt){
    evt.preventDefault();
    if(productsCollected){
        emptyRows();
    }
    if(productsCollected == false){
        collectProducts();
        productsCollected = true;
    }

    fillCatList();
    chosenCats = filertList(catList);
    buildCategoryPage(chosenCats,productMap);
})
$clearButton.on('click', function(evt){
    uncheckAllBoxes();
    if(productsCollected){
        emptyRows();
    }
    if(productsCollected == false){
        collectProducts();
        productsCollected = true;
    }

    fillCatList();
    chosenCats = filertList(catList);
    buildCategoryPage(chosenCats,productMap);
})

/**
 * This function detaches all products from the page and stores them
 * in a map using the product.id as the key and the html content as the
 * product.
 */
function collectProducts(){
    
    $allCards = $('.col-3.d-flex.justify-content-center.m-0');
    for(let card of $allCards){
        productIdList.push(card.id);
    }
    for(let id of productIdList){
        productList.push($(`#${id}`).detach())
    }
    fillProductMap(productList);
}

function fillProductMap(products){
    for(let product of products){
        productMap.set(product.attr('id'), product);
    }
}

/**
 * This function uses checkMatch to see which products match the user's
 * selections. Then it appends the product to a row. It also makes sure
 * that each row has no more than 4 products.
 */
function buildCategoryPage(categories, product_Map){
    let matchedList = []
    let interval = 4;
    let count = 0;
    for(let product of product_Map.keys()){
        if(checkMatch(product_Map.get(product),categories)){
            matchedList.push(product_Map.get(product));  
        }
    }
    if(matchedList.length > 0){
        if($notFound.css('display') == 'block'){
            $notFound.toggle();
        }
        for(let row of $theRows){
            while(count < interval){
                if(matchedList[count]){
                    row.append(matchedList[count][0]);
                }
                count++;
            }
            interval = interval + 4;
        }
    }
    else{
        if($notFound.css('display') == 'none'){
            $notFound.toggle();
        }
    }
}
/**
 * This function identifies what products match the users category selections
 */
function checkMatch(element,categories){
    for(let cat of categories){
        if(cat == element.data('category')){
            return true;
        }
    }
}
function uncheckAllBoxes(){
    $plateCheckBox.prop('checked',false);
    $bowlCheckBox.prop('checked',false);
    $trayCheckBox.prop('checked',false);
    $basketCheckBox.prop('checked',false);
    $miscCheckBox.prop('checked',false);
    $signCheckBox.prop('checked',false);
    $furnitureCheckBox.prop('checked',false);
    $boxCheckBox.prop('checked',false);
}
/**
 * This function clears $theRows so the selected products can be added to the 
 * rows
 */
function emptyRows(){
    for(let row of $theRows){
        while(row.firstChild){
            row.removeChild(row.firstChild);
        }
    }
}

/**
 * This function returns a list of values that have been identified as the 
 * categories the user has chosen
 */
function filertList(list){
    let returnlist = [];
    for(let item of list){
        if(item['value']){
            returnlist.push(item['name']);
        }
    }
    //if the user deslects all the categories then this will override
    //and fill the return list with all categories
    if(returnlist.length < 1){
        for(let item of list){
            returnlist.push(item['name']);
        }
    }
    
    return returnlist;
}

/**
 * This function builds a list of object key/value pairs
 */
function fillCatList(){
        catList = [{'name':'plate','value': $plateCheckBox.prop('checked')},
        {'name':'bowl','value':$bowlCheckBox.prop('checked')},
        {'name':'tray','value':$trayCheckBox.prop('checked')}, 
        {'name':'basket','value':$basketCheckBox.prop('checked')},
        {'name':'miscellaneous','value':$miscCheckBox.prop('checked')},
        {'name':'sign','value':$signCheckBox.prop('checked')},
        {'name':'furniture','value':$furnitureCheckBox.prop('checked')},
        {'name':'box','value':$boxCheckBox.prop('checked')}];

}