import { fetchJson } from '../../lib/api';

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

/**
 * Retrieves the count of records based on the specified language.
 *
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 */
export default async function handler(req, res) {
  const { method } = req;
  const { Language } = req.query;

  if (method === 'GET') {
    try {
      // Fetch data from the API endpoint
      const jsonData = await fetchJson(`${apiUrl}/count_records/${Language}`);
      
      // Return the retrieved data as the response
      res.status(200).json(jsonData);
    } catch (error) {
      // Handle errors during data retrieval
      res.status(500).json({ message: 'Error while loading the data.' });
    }
  } else {
    // Handle invalid request methods
    res.status(405).json({ message: 'Method not allowed.' });
  }
}
