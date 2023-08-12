import React from "react";

/**
 * The PDFViewer component displays a button that opens a PDF file in a new window when clicked.
 *
 * @returns {JSX.Element} The PDFViewer component.
 */
const PDFViewer = () => {
  const pdfPath = "/pdf/_userManuel.pdf"; // Path to the PDF file in the `public` directory

  /**
   * Handles the button click event. Opens the PDF file in a new window.
   */
  const handleButtonClick = () => {
    window.open(pdfPath, "PDF-Window");
  };

  return (
    <div>
      {/* Button to open the PDF */}
      <button onClick={handleButtonClick}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="30"
          height="30"
          viewBox="0 0 24 24"
          fill="none"
          stroke="white"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="feather feather-info"
        >
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="16" x2="12" y2="12"></line>
          <line x1="12" y1="8" x2="12.01" y2="8"></line>
        </svg>
      </button>
    </div>
  );
};

export default PDFViewer;
