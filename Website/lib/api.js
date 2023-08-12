/**
 * Fetches JSON data from the specified URL.
 *
 * @param {string} url - The URL to fetch JSON data from.
 * @returns {Promise} - A promise that resolves to the fetched JSON data.
 * @throws {Error} - If the request fails or the response status is not ok.
 */
export async function fetchJson(url) {
	const response = await fetch(url);
	if (!response.ok) {
	  throw new Error(`Request failed: ${response.status}`);
	}
	return await response.json();
  }
  
  /**
   * Fetches text data from the specified URL.
   *
   * @param {string} url - The URL to fetch text data from.
   * @returns {Promise} - A promise that resolves to the fetched text data.
   * @throws {Error} - If the request fails or the response status is not ok.
   */
  export async function fetchTxt(url) {
	const response = await fetch(url);
	if (!response.ok) {
	  throw new Error(`Request failed: ${response.status}`);
	}
	return await response.text();
  }
  
  /**
   * Fetches JSON data from the specified URL using custom options.
   *
   * @param {string} url - The URL to fetch JSON data from.
   * @param {object} options - Additional options for the fetch request.
   * @returns {Promise} - A promise that resolves to the fetched JSON data.
   * @throws {ApiError} - If the request fails or the response status is not ok.
   */
  export async function fetchJsonNew(url, options) {
	const response = await fetch(url, options);
	if (!response.ok) {
	  throw new ApiError(url, response.status);
	}
	const jsonData = await response.json();
	return jsonData;
  }
  
  /**
   * Custom error class for API errors.
   */
  export class ApiError extends Error {
	constructor(url, status) {
	  super(`'${url}' returned ${status}`);
	  if (Error.captureStackTrace) {
		Error.captureStackTrace(this, ApiError);
	  }
	  this.name = 'ApiError';
	  this.status = status;
	}
  }
  