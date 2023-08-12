import { useState } from 'react';

//The component provides a way to render a column with keywords that can be expanded or collapsed.
// When the button is clicked, the isOpen state is toggled, and the list of keywords is displayed or hidden accordingly.
// This allows users to easily view or hide the keywords associated with the column.

const KeywordsColumn = ({ label, keywords }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleOpen = () => {
    setIsOpen(!isOpen);
  };
  return (
    <div>
      <button
        onClick={toggleOpen}
        className="text-blue-500 hover:underline"
      >
        {label} ({isOpen ? '-' : '+'})
      </button>

      {isOpen && (
        <ul className="mt-2">
          {keywords.map((keyword, index) => (
            <li key={index} className="ml-4">
              {keyword}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default KeywordsColumn;