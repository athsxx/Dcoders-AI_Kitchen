document.getElementById('recipe-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const recipeName = document.getElementById('recipe-name').value;
    
    fetch('/analyze_recipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ recipe_name: recipeName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            document.getElementById('ingredients-list').innerHTML = data.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('');
            document.getElementById('utensils-list').innerHTML = data.utensils.map(utensil => `<li>${utensil}</li>`).join('');
            document.getElementById('instructions-list').innerHTML = data.instructions.map(instruction => `<li>${instruction}</li>`).join('');
            
            document.getElementById('results').classList.remove('hidden');
            document.getElementById('audio-player').src = '/get_speech';
            document.getElementById('audio-player').classList.remove('hidden');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
