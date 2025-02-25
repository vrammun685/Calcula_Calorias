const cantidad = document.getElementById('cantidad');
const calorias = document.getElementById('calorias');
const data_calorias = cantidad.getAttribute("data-calorias")
cantidad.addEventListener("input", function() {
    calorias.value =(data_calorias*this.value)/100;
});