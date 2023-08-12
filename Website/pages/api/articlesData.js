import { fetchJson, fetchJsonNew } from '../../lib/api';

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

/**
 * Pauses the function for the specified number of milliseconds.
 *
 * @param {number} milliseconds - The number of milliseconds to pause.
 * @returns {Promise} - A promise that resolves after the specified time.
 */
function Sleep(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

async function test() {
  await Sleep(500); // Pause the function for 500 milliseconds (0.5 seconds)
}

/**
 * Strips unnecessary data from the article object.
 *
 * @param {Object} article - The article object to be stripped.
 * @returns {Object} - The stripped article object.
 */
function stripArticle(article) {
  const stripDate = (date, language, url) => {
    if (language === 'Ukranian' && url.includes('https://www.helsinki.org.ua')) {
      return date.substr(0, 15);
    } else {
      return date;
    }
  };

  return {
    id: article.id,
    title: article.title,
    Priority: article.Priority,
    DatePublication: stripDate(article.DatePublication, article.Language, article.Url),
    Language: article.Language,
    Url: article.Url,
    Actors: [...article.Actors],
    Location: [...article.Location],
    Organizations: [...article.Organizations],
    IDPMatchedKeywords: [...article.IDPMatchedKeywords],
    CatagoryMatchedKeywords: [...article.CatagoryMatchedKeywords],
    LocalPath: article.LocalPath,
    KeyWords: [...article.KeyWords],
    Category: [...article.Category],
  };
}

/**
 * Retrieves filtered records based on the specified query parameters.
 *
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 */
export default async function handler(req, res) {
  console.log('--- handler ---');
  await test();

  const { page, pageSize, Language, Category, Priority } = req.query;
  const { method } = req;

  console.log("QUERY PARAMETERS");
  console.log("page:", page);         // Example: "2"
  console.log("pageSize:", pageSize); // Example: "10"
  console.log("Language:", Language); // Example: "Azerbaijani"
  console.log("Category:", Category); // Example: "Category Cash benefits OR Second"
  console.log("Priority:", Priority); // Example: "3.5"
  console.log(typeof Priority);

  if (method === 'GET') {
    try {
      // Read data

      // POST request to the backend
      const urlString = `${apiUrl}/filter_records?page=${page}&page_size=${pageSize}`;
      const bodyObj = { Language: Language };

      if (Category) {
        bodyObj.Category = Category.split(" OR ");
      }

      if (Priority) {
        bodyObj.Priority = parseFloat(Priority);
      }

      let jsonData = await fetchJsonNew(urlString, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(bodyObj),
      });

      // Sort records by priority in descending order
      const sortedRecords = jsonData.records.sort((a, b) => {
        return b.Priority - a.Priority;
      });
      jsonData.records = sortedRecords;

      // Strip unnecessary data from the records
      const stripedRecords = jsonData.records.map(stripArticle);
      jsonData.records = stripedRecords;

      // Return the filtered and stripped records as the response
      res.status(200).json(jsonData);

    } catch (error) {
      // Handle errors during data retrieval
      res.status(500).json({ message: 'Error when loading the data.' });
    }
  } else {
    // Handle invalid request methods
    res.status(405).json({ message: 'Method not allowed.' });
  }
}

