import React from "react";

/**
 * The TitleButton component displays a button with a title.
 *
 * @param {React.ReactNode} children - The content to be displayed within the button.
 * @returns {JSX.Element} The TitleButton component.
 */
const TitleButton = ({ children }) => {
  return (
    <button
      className="flex flex-row justify-center items-center p-2 space-x-2 w-32 h-9 bg-white rounded-lg shadow-blue-200 shadow-sm"
    >
      {children}
    </button>
  );
};

export default TitleButton;

