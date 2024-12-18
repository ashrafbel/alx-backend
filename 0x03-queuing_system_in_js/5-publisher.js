const rs = require('redis');


const clientRedis = rs.createClient();

clientRedis.on('connect', () => {
    console.log('Redis client connected to the server');
});

clientRedis.on('error', (err) => {
    console.log('Redis client not connected to the server: ' + err);
});

function publishMessage(message, time) {
    setTimeout(() => {
        console.log(`About to send ${message}`);
        clientRedis.publish('holberton school channel', message);
    }, time);
}

publishMessage("Holberton Student #1 starts course", 100);
publishMessage("Holberton Student #2 starts course", 200);
publishMessage("KILL_SERVER", 300);
publishMessage("Holberton Student #3 starts course", 400);
