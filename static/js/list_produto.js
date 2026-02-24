const container = document.querySelector('.creation-product-container')
const creationform = document.getElementById('form-creation-product')
const creationshowup = document.getElementById('add-produto-button') 

creationshowup.addEventListener('click', () => {
    
    container.classList.toggle('active')
})

container.addEventListener('click', (e) => {

    if (e.target === container) {

        container.classList.toggle('active')
    }
})

creationform.addEventListener('submit', async (e) => {

    e.preventDefault() 

    const data = new FormData(creationform)

    try {
        const res = await fetch(creationform.getAttribute('creation_url'), {
            
            method: 'POST',
            body: data
            
        })

        if(res.ok){
            window.location.reload()
            return
        }

        throw Error('bad request error')
    } catch (error) {
        alert('failure while processing request')
    }
})