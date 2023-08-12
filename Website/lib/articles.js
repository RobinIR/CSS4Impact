import { fetchJson } from './api';

const CMS_URL = 'http://localhost:8000';

/**
 * Deprecated. Changed to API Routes 
 * Retrieves an article by its ID.
 *
 * @param {string} id - The ID of the article to retrieve.
 * @returns {Promise} - A promise that resolves to the retrieved article.
 */
export async function getArticle(id) {
  const article = await fetchJson(`${CMS_URL}/collection/${id}`);
  return stripArticle(article);
}

/**
 * Retrieves all articles.
 *
 * @returns {Promise} - A promise that resolves to an array of articles.
 */
export async function getArticles() {
  console.log('GET ALL ARTICLES!');
  const articles = await fetchJson(`${CMS_URL}/collection/path`);
  return articles.map(stripArticle);
}

/**
 * Retrieves articles by language.
 *
 * @param {string} language - The language of the articles to retrieve.
 * @returns {Promise} - A promise that resolves to an array of articles.
 */
export async function getArticlesByLanguage(language) {
  console.log('GET ALL ARTICLES!');
  const articles = await fetchJson(`${CMS_URL}/collection/path/${language}`);
  return articles.map(stripArticle);
}

/**
 * Retrieves articles based on filter options.
 *
 * @param {object} filterOptions - The filter options to apply.
 * @returns {Promise} - A promise that resolves to an array of articles.
 */
export async function getArticlesByFilterOptions(filterOptions) {
  console.log('GET ALL ARTICLES!');
  const articles = await fetchJson(`${CMS_URL}/collection/path/${filterOptions.language}`);
  return articles;
}

/**
 * Extracts the desired data from an article.
 *
 * @param {object} article - The article object to extract data from.
 * @returns {object} - The extracted data object.
 */
function stripArticle(article) {
  return {
    id: article.id,
    title: article.title,
    priority: article.priority,
  };
}
