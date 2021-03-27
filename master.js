let myButton = document.querySelector('button');

myButton.onclick = function() {
    addfight() 
    $.ajax({
        url: '/fightclub/fightclub_api.py'
        type: 'GET',
        success: function (response) {
            console.log(response);
        }
  }

