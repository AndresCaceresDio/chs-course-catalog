document.getElementById('hinkPinkForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/submit-hink-pink', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = data.message;
    })
    .catch(error => console.error('Error:', error));
});

function toggleExample() {
    var example = document.getElementById('example');
    if (example.classList.contains('hidden')) {
        example.classList.remove('hidden');
    } else {
        example.classList.add('hidden');
    }
};
