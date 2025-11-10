// marcarlisto.js
document.addEventListener("DOMContentLoaded", () => {
    const botonesListo = document.querySelectorAll(".boton-listo");

    if (botonesListo.length === 0) return;

    botonesListo.forEach(boton => {
        boton.addEventListener("click", function (event) {
            event.preventDefault(); // evita enviar el form de inmediato

            Swal.fire({
                title: "¡Reservación completada!",
                text: "La reservación fue marcada como 'Listo' con éxito.",
                imageUrl: "https://i.gifer.com/Fhhu.gif",
                imageWidth: 200,
                imageHeight: 150,
                confirmButtonText: "OK",
                confirmButtonColor: "#4CAF50"
            }).then(() => {
                this.closest("form").submit(); // envía el form tras la alerta
            });
        });
    });
});
