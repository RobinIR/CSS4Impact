import React, { useState } from "react";

//CopyOnClick component renders a button that, when clicked, copies the specified file path to the clipboard using the navigator.clipboard.writeText() method.

const CopyOnClick = ({ filePath }) => {
 
  const handleCopyClick = async () => {
    navigator.clipboard
      .writeText(filePath)
      .then(() => {
        console.log("Text wurde erfolgreich kopiert");
      })
      .catch((error) => {
        console.error("Fehler beim Kopieren des Textes:", error);
      });
  };

  return (
    <div>
    <button onClick={handleCopyClick} className="text-xs hover:text-blue-500" >
    {filePath}
    </button>
    </div>
  );
};

export default CopyOnClick;
