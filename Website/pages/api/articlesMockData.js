import fs from 'fs';
import path from 'path';

/**
 * Pauses the function for the specified number of milliseconds.
 *
 * @param {number} milliseconds - The number of milliseconds to pause.
 * @returns {Promise} - A promise that resolves after the specified time.
 */
function Sleep(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

/**
 * Tests the sleep function by pausing for 2 seconds.
 */
async function test() {
  await Sleep(2000); // Pause the function for 2000 milliseconds (2 seconds)
}

/**
 * Retrieves filtered and paginated data from a mock data file.
 *
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 */
export default async function handler(req, res) {
  console.log('--- handler ---');
  await test();

  const { page, pageSize, sort, Language } = req.query;
  const { method } = req;

  const dataFilePath = path.join(process.cwd(), 'data/articles-mock-data.json');

  if (method === 'GET') {
    try {
      // Read mock data from file
      const fileContent = fs.readFileSync(dataFilePath, 'utf-8');
      let jsonData = JSON.parse(fileContent);
      let filteredJsonData = [];
      let sortedJsonData = [];
      let pageJsonData = [];

      if (Language) {
        // Filter data based on language
        filteredJsonData = jsonData.filter((item) => item.Language === Language);
        jsonData = filteredJsonData;
      }

      if (sort) {
        // Sort data based on the specified field
        sortedJsonData = jsonData.sort((a, b) => {
          const t = typeof a[sort];
          if (t === 'number') {
            return a[sort] - b[sort];
          } else {
            const nameA = a[sort].toLowerCase();
            const nameB = b[sort].toLowerCase();
            if (nameA < nameB) {
              return -1;
            }
            if (nameA > nameB) {
              return 1;
            }
            return 0;
          }
        });
        jsonData = sortedJsonData;
      }

      const pS = parseInt(pageSize);
      const p = parseInt(page);
      const from = (p - 1) * pS;
      let to = from + pS - 1;
      if (to >= jsonData.length - 1) {
        to = jsonData.length - 1;
      }

      // Paginate data based on the specified page and page size
      pageJsonData = jsonData.slice(from, to + 1);
      res.status(200).json(pageJsonData);

    } catch (error) {
      res.status(500).json({ message: 'Error when loading the data.' });
    }
  } else {
    res.status(405).json({ message: 'Method not allowed.' });
  }
}
