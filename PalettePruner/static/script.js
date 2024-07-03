document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData();
    var fileInput = document.getElementById('file-input');
    formData.append('file', fileInput.files[0]);

    document.querySelector('button[type="submit"]').style.display = 'none';
    document.getElementById('upload-loading').style.display = 'block';
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('button[type="submit"]').style.display = 'block';
        document.getElementById('upload-loading').style.display = 'none';
        if (data.error) {
            alert(data.error);
        } else {
            var colorList = document.getElementById('color-list');
            var categorySelect = document.getElementById('category-select');
            colorList.innerHTML = '';
            categorySelect.innerHTML = '';

            Object.keys(data.color_dict).forEach(category => {
                var li = document.createElement('li');
                var colorSample = document.createElement('span');
                colorSample.style.display = 'inline-block';
                colorSample.style.width = '20px';
                colorSample.style.height = '20px';
                colorSample.style.backgroundColor = data.color_dict[category][0];
                colorSample.style.marginRight = '10px';
                li.appendChild(colorSample);
                li.appendChild(document.createTextNode(`${category}: ${data.color_dict[category].length} colors`));
                colorList.appendChild(li);
                
                var option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                categorySelect.appendChild(option);
            });

            document.getElementById('color-categories').style.display = 'block';
            document.getElementById('result').style.display = 'none';
        }
    });
});

document.getElementById('remove-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var selectedCategories = Array.from(document.getElementById('category-select').selectedOptions).map(option => option.value);
    var filename = document.getElementById('file-input').files[0].name;

    document.querySelector('#remove-form button[type="submit"]').style.display = 'none';
    document.getElementById('remove-loading').style.display = 'block';

    fetch('/remove', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ categories: selectedCategories, filename: filename })
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('#remove-form button[type="submit"]').style.display = 'block';
        document.getElementById('remove-loading').style.display = 'none';
        if (data.error) {
            alert(data.error);
        } else {
            var outputImage = document.getElementById('output-image');
            outputImage.src = `/uploads/${data.output_filename}`;
            document.getElementById('result').style.display = 'block';
        }
    });
});
