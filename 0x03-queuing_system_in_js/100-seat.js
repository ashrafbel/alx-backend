import express from 'express';
import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';

const client = redis.createClient();

const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

const queue = kue.createQueue();

let reservationEnabled = true;

async function reserveSeat(number) {
    await setAsync('available_seats', number.toString());
}

async function getCurrentAvailableSeats() {
    const seats = await getAsync('available_seats');
    return seats ? parseInt(seats) : 0;
}

const app = express();
const PORT = 1245;

async function initializeSeats() {
    await reserveSeat(50);
}
initializeSeats();

app.get('/available_seats', async (req, res) => {
    const numberOfAvailableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: numberOfAvailableSeats.toString() });
});

app.get('/reserve_seat', (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: 'Reservation are blocked' });
    }

    const job = queue.create('reserve_seat', {}).save((err) => {
        if (err) {
            return res.json({ status: 'Reservation failed' });
        }
        res.json({ status: 'Reservation in process' });
    });

    job.on('complete', (result) => {
        console.log(`Seat reservation job ${job.id} completed`);
    });

    job.on('failed', (errorMessage) => {
        console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
    });
});

app.get('/process', (req, res) => {
    res.json({ status: 'Queue processing' });

    queue.process('reserve_seat', async (job, done) => {
        const availableSeats = await getCurrentAvailableSeats();

        if (availableSeats <= 0) {
            reservationEnabled = false;
            return done(new Error('Not enough seats available'));
        }

        const newAvailableSeats = availableSeats - 1;
        await reserveSeat(newAvailableSeats);
        if (newAvailableSeats === 0) {
            reservationEnabled = false;
        }

        done();
    });
});


app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

client.on('error', (err) => {
    console.error('Redis Client Error', err);
});
