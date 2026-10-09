const imgbomb = document.getElementById('imgbomb');
const btnOn = document.getElementById('on');
const btnOff = document.getElementById('off');
const Contador = document.getElementById('contador');
const ESP_32 = "http://10.232.204.231";

function logToConsole(message) {
            const consoleOutput = document.getElementById('console');
            
            const line = document.createElement('div');
            line.classList.add('console-line');
            
            const time = new Date().toLocaleTimeString();
            line.textContent = `[${time}] ${message}`;

            consoleOutput.appendChild(line);
            consoleOutput.scrollTop = consoleOutput.scrollHeight;
        }

let contador = 0
urlOn = 'img/bombon.png';
urloff = 'img/bomboff.png';

btnOn.addEventListener('click', async() => {
    try {
        const respuesta = await fetch(`${ESP_32}/on`);//thonny
        
        if (respuesta.ok){
            const datos = await respuesta.text();
            console.log('Respuesta ESP32:', datos);
            contador++;
            Contador.textContent=String(contador).padStart(2, "0");
            logToConsole(datos);
            imgbomb.src=urlOn;
            imgbomb.alt='Bombillo Encendido';
        }
        
    
    } catch (error){
        console.error('Error al comunicarse con el servidor ESP32', error);
    } 
});
btnOff.addEventListener('click', async() => {
    try {
        const respuesta = await fetch(`${ESP_32}/off`);//thonny
        if (respuesta.ok){
            const datos = await respuesta.text();
            console.log('Respuesta ESP32:', datos);
            logToConsole(datos);
            imgbomb.src=urloff;
            imgbomb.alt='Bombillo Apagado';
        }
    
    } catch (error){
        console.error('Error al comunicarse con el servidor ESP32', error);
    }
});


