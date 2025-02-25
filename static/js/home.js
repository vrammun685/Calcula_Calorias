document.addEventListener('DOMContentLoaded', function(){
    const canva = document.getElementById('caloriasCanva');
    const calorias_consumidas = parseInt(canva.getAttribute('data-consumidas'));
    const calorias_totales = parseInt(canva.getAttribute('data-total'));
    const calorias_restantes = parseInt(canva.getAttribute('data-restantes'));

    var ctx = canva.getContext('2d');

    // Crear el gráfico
    var caloriasChart = new Chart(ctx, {
        type: 'doughnut',  // Tipo de gráfico
        data: {
            labels: ['Consumidas', 'Restantes'],  // Etiquetas para las secciones del gráfico
            datasets: [{
                data: [calorias_consumidas, calorias_restantes],  // Los datos para el gráfico
                backgroundColor: ['rgb(51, 255, 129)', '#FF5733'],  // Colores de cada segmento
                hoverBackgroundColor: ['#ff4d6d', '#2680c2'],  // Colores al pasar el mouse
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'  // Posición de la leyenda
                }
            },
            cutout: 100,
        }
    });
});