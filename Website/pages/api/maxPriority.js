import { fetchJson } from "../../lib/api";

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

/**
 * Handler function to retrieve collection data by priority and language.
 *
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 */
export default async function handler(req, res) {
  const { method } = req;
  const { Language } = req.query;

  if (method === "GET") {
    try {
      // Read data from the API endpoint
      let jsonData = await fetchJson(
        `${apiUrl}/collection/priority/${Language}`
      );

      // Return the data as a response
      res.status(200).json(jsonData);
    } catch (error) {
      res.status(500).json({ message: "Error when loading the data." });
    }
  } else {
    res.status(405).json({ message: "Method not allowed." });
  }
}
