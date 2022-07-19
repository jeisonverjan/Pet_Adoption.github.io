country_select = document.getElementById('country');
state_select = document.getElementById('state');
city_select = document.getElementById('city');
       
country_select.onchange = function(){
    country = country_select.value;
        
    fetch('state/' + country).then(function(response){
        response.json().then(function(data) {
            optionHTML = '';
            for (state of data.statecountry) {
            optionHTML += '<option value="' + state.id +'">' + state.name + '</option>'
            }
           state_select.innerHTML = optionHTML;
          });
       });
      }

state_select.onchange = function(){
    city = state_select.value; 
    fetch('city/' + city).then(function(response){
        response.json().then(function(data) {
          optionHTML = '';
          for (city_rs of data.citylist) {
          optionHTML += '<option value="' + city_rs.id +'">' + city_rs.name + '</option>'
          }
        city_select.innerHTML = optionHTML;
        });
      });
    }