import { useState } from 'react';

/**
 * Custom hook for managing column toggles.
 * This hook provides functionality to manage column toggles,
 * including accessing the current column state and toggling columns.
 *
 * @param {Array} initialColumns - The initial column configuration.
 * @returns {Object} - An object containing the columns and toggle function.
 */
const useColumnToggle = (initialColumns) => {
  const [columns, setColumns] = useState(initialColumns);

  /**
   * Toggle the state of a column.
   *
   * @param {string} name - The name of the column to toggle.
   */
  const handleColumnToggle = (name) => {
    setColumns((prevItems) => {
      const updatedColumns = prevItems.map((item) => ({
        ...item,
        checked: item.name === name ? !item.checked : item.checked,
      }));
      return updatedColumns;
    });
  };

  return { columns, handleColumnToggle };
};

export default useColumnToggle;

