const redis = require('redis');
const { promisify } = require('util');

const client = redis.createClient();

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

async function displaySchoolValue() {
    try {
        console.log('School');
        
        const setReply = await setAsync('School', '100');
        console.log('Reply:', setReply);

        const reply = await getAsync('School');
        console.log(reply);
    } catch (error) {
        console.error('Error:', error);
    }
}

displaySchoolValue();
