const order_button = document.getElementById('item-order-but')
const purchase_button = document.getElementById('item-purchase-but')
const quantity_input = document.getElementById('quantity-item-input')

order_button.addEventListener('click', async () => {

    let quantity = quantity_input.value

    const final_url = new URL(pedido_url_base, window.location.origin)
    final_url.searchParams.set('quantity', quantity)

    const res = await fetch(final_url, {method:'post'}) 

    if (res.ok) {
        const data = await res.json()
        return window.location.href = data.url
    }

    alert('ocorreu algum erro interno, por favor, tente novamente mais tarde')
})

purchase_button.addEventListener('click', async () => {

    let quantity = quantity_input.value

    const final_url = new URL(pedido_url_base)
    final_url.searchParams.set('pay_now','true')
    final_url.searchParams.set('quantity', quantity)

    const res = await fetch(final_url, {method:'post'}) 

    if (res.ok) {
        const data = await res.json()
        console.log(data)
        return window.location.href = data.url
    }
    alert('ocorreu algum erro interno, por favor, tente novamente mais tarde')
})