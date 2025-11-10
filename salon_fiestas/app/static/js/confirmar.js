function confirmarEliminacion(event) {
    event.preventDefault(); // esto hace que evite que se vaya al url de volada

    const url = event.currentTarget.href; // en esta variable se guarda la  url 

    Swal.fire({
        title: '¿Estás seguro?',
        html: `
        <p><strong>ALTOOOO</strong> relaja la tupla  ¿seguro que quieres eliminar la reservación?</p>
        <img src="https://media1.tenor.com/m/kTohyd7QJNwAAAAC/stop-seong-gi-hun.gif" 
         width="200" height="150" style="border-radius:10px; margin-top:10px;">`,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {

            Swal.fire({
                title: "Borrado con éxito",
                html: `
                <p>Te extrañaremos... :c </p>
                <img src="https://media.tenor.com/KyTSHBMDmMIAAAAM/cat-crying-cat.gif" 
                width="200" height="150" style="border-radius:10px; margin-top:10px;">`,
                showConfirmButton: false,
                timer: 1500, // la alerta se cierra automáticamente después de 1.5s
                willClose: () => {
                    window.location.href = url; // redirige después de cerrarse
                }
            });
        }
    });

    return false;
}



document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get("exito") === "1") {
        Swal.fire({
            title: "¡Operación realizada correctamente!",
            html: `
                <p>La reservación fue procesada correctamente</p>
                <img src="https://media.tenor.com/Xt80NIhpKnIAAAAM/jh.gif"
                width="200" height="150" style="border-radius:10px; margin-top:10px;">`,
            icon: "success",
            confirmButtonText: "OK"
        }).then(() => {
            event.target.submit(); // ahora sí se envía el form a django
        });
    }
});


