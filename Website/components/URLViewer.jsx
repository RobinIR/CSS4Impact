import React from "react";

/**
 * The URLViewer component displays a button that opens a URL in a new window.
 *
 * @param {string} url - The URL to be opened in the new window.
 * @returns {JSX.Element} The URLViewer component.
 */
const URLViewer = ({ url }) => {
  const hexColor = "#4676FB";

  /**
   * Handles the button click event and opens the URL in a new window.
   */
  const handleButtonClick = () => {
    window.open(url, "HTML-Viewer");
  };

  return (
    <div>
      <button onClick={handleButtonClick}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke={hexColor}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="feather feather-globe"
        >
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="2" y1="12" x2="22" y2="12"></line>
          <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
        </svg>
      </button>
    </div>
  );
};

export default URLViewer;
