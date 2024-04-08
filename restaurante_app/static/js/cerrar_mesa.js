document.addEventListener('DOMContentLoaded', function() {
    const cerrarMesaButtons = document.querySelectorAll('.cerrar-mesa-btn');

    cerrarMesaButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const mesaId = btn.dataset.mesaid;
            fetch(`/cerrar_mesa_detalle/${mesaId}`)
                .then(response => response.json())
                .then(data => {
                    // Mostrar los detalles de la mesa en una ventana emergente
                    alert(`Detalles de la mesa:\nNombre: ${data.mesa}\nTotal: ${data.total}`);
                })
                .catch(error => console.error('Error al obtener los detalles de la mesa:', error));
        });
    });
});
