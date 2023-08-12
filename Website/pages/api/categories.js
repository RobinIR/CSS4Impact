import { fetchJson } from '../../lib/api';

/**
 * Strips the category property from an object.
 *
 * @param {Object} obj - The object to strip the category property from.
 * @returns {string} - The stripped category value.
 */
function stripCategory(obj) {
  return obj.category;
}

/**
 * Retrieves the category data from the backend.
 *
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 */
export default async function handler(req, res) {
  const { method } = req;
  const { Language } = req.query;

  if (method === 'GET') {
    try {
      // Read category data from the backend
      let jsonData = await fetchJson(`${process.env.NEXT_PUBLIC_API_URL}/category/path/${Language}`);
      
      // Strip the unnecessary data for frontend
      const strippedData = jsonData.map(stripCategory);
      
      res.status(200).json(strippedData);
    } catch (error) {
      res.status(500).json({ message: 'Error reading data!' });
    }
  } else {
    res.status(405).json({ message: 'Method not allowed!' });
  }
}
