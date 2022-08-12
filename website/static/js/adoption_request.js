pet_name = document.getElementById('pet_name');
pet_type = document.getElementById('pet_type');
pet_breed = document.getElementById('pet_breed');
pet_city = document.getElementById('pet_city');
pet_age = document.getElementById('pet_age');
pet_sex = document.getElementById('pet_sex');

function adoption_request(postId){
  
  localStorage.setItem("textvalue", postId)
  
  window.location.href = "/adoption_request";
  return false;
  
}

let postId = localStorage.getItem("textvalue");

fetch("/pet_info", {
  method: "POST",
  body: JSON.stringify({ postId: postId }),
}).then(function(response){
  response.json().then(function(data){
    for (pet of data.postObject){
      pet_type.value = pet.pet_type_name
      pet_name.value = pet.pet_name
      pet_breed.value = pet.breed_name
      pet_city.value = pet.city_name
      pet_age.value = pet.pet_age
      pet_sex.value = pet.pet_sex
    }
    
  })
})