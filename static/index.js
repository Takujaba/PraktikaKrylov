
const resultDiv = document.querySelector('.result')
const form = document.querySelector('.send_form')

form.addEventListener('submit', (e) => {
    e.preventDefault()
    resultDiv.innerHTML = ''
    resultDiv.innerHTML = 'Обработка...'

    const file = document.querySelector('.upload_image_input').files[0]
    const formData = new FormData()
    formData.append('image', file)

    fetch(
        location.protocol + '//' + location.hostname + ':' + location.port + '/',
        {
            method: 'POST',
            body: formData
        }
    )
        .then(res => res.json())
        .then(res => {
            resultDiv.innerHTML = ''
            const h3 = document.createElement('h3')
            h3.innerHTML = 'Всего овец найдено: ' + res.sheep_count
            const image = document.createElement('img')
            image.src = res.image
            console.log(res.image);
            
            resultDiv.appendChild(h3)
            resultDiv.appendChild(image)
        })
        .catch(err => {
            console.log(err)
            resultDiv.innerHTML = 'Ошибка запроса'
        })
})
