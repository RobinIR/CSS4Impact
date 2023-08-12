import path from 'path';

/**
 * Handler function to retrieve the desktop path.
 * It's important to note that this component is defined but not currently being used or rendered in any other component.
 * See FileViewer.js
 *
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 */
export default function handler(req, res) {
  const desktopPath = path.join(
    process.env.HOME || process.env.USERPROFILE,
    'Desktop'
  );

  // Return the desktop path
  res.status(200).json({ desktopPath });
}
