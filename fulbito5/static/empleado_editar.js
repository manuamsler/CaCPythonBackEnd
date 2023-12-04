console.log(location.search); // Lee los argumentos pasados a este formulario
var id = location.search.substr(4);
console.log(id);

const { createApp } = Vue;

createApp({
    data() {
        return {
            id: 0,
            nombre: "",
            apellido: "",
            whatsapp: "",
            posicion: "",
           
          
            url: 'http://localhost:5000/empleados/' + id,
        };
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    this.id = data.id;
                    this.nombre = data.nombre;
                    this.apellido = data.apellido;
                    this.whatsapp = data.whatsapp;
                    this.posicion = data.posicion;
                    
                })
                .catch(err => {
                    console.error(err);
                    this.error = true;
                });
        },
        modificar() {
            let empleado = {
                nombre: this.nombre,
                apellido: this.apellido,
                whatsapp: this.whatsapp,
                posicion: this.posicion,
                
            };
            var options = {
                body: JSON.stringify(empleado),
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            };
            fetch(this.url, options)
                .then(function () {
                    alert("Registro modificado");
                    window.location.href = "./index.html";
                })
                .catch(err => {
                    console.error(err);
                    alert("Error al Modificar");
                });
        }
    },
    created() {
        this.fetchData(this.url);
    },
}).mount('#app');