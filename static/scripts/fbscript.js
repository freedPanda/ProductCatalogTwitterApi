const $fbButton = $('#moretesting');
var $fbEvent = '';

function tester(){
    console.log($fbButton);
};

$(document).ready(function(evt){
    FB.Event.bind({
        'share':
        function(evt){
            console.log('stuffing it');
        }
    });
});

$fbButton.on('click', function(evt){
    console.log('stuffing');
});


