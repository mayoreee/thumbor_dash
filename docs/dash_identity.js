const Dash = require('dash');

const clientOpts = {
  apps: {
    tutorialContract: {
      contractId: 'GARueEFPo9dX1teXpmhvfzEB1ZVYi5SyvyYPWpU1cipq',
    },
  },
};
const client = new Dash.Client(clientOpts);

const getDocuments = async () => {
  return client.platform.documents.get(
    'tutorialContract.documents',
    {
      limit: 2, // Only retrieve 1 document
    },
  );
};

getDocuments()
  .then((d) => console.dir(d))
  .catch((e) => console.error('Something went wrong:\n', e))
  .finally(() => client.disconnect());