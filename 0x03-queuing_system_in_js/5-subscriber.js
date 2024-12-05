const redis = require('redis');

const clientRedis = redis.createClient();


clientRedis.on('connect', () => {
    console.log('Redis client connected to the server');
});

clientRedis.on('error', (err) => {
    console.log('Redis client not connected to the server: ' + err);
});

clientRedis.subscribe('holberton school channel');

clientRedis.on('message', (channel, message) => {
    console.log(message);
    if (message === 'KILL_SERVER') {
        clientRedis.unsubscribe();
        clientRedis.quit();
    }
});
