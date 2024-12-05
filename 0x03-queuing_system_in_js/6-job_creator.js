const kue = require('kue');

const queue = kue.createQueue();

const dataJob = {
  phoneNumber: '1234567890',
  message: 'Hello from Holberton!',
};

const job = queue.create('push_notification_code', dataJob)
  .save((err) => {
    if (err) {
      console.log('Error creating job:', err);
    } else {
      console.log(`Notification job created: ${job.id}`);
    }
  });

job.on('complete', () => {
  console.log('Notification job completed');
});

job.on('failed', (errorMessage) => {
  console.log('Notification job failed:', errorMessage);
});
