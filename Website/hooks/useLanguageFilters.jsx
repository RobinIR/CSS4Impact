import { useState } from 'react';

/**
 * Custom hook for managing language filters.
 * This hook provides functionality to manage language filters,
 * including accessing the current language filter state and toggling filters.
 *
 * @param {Array} initialFilters - The initial language filter configuration.
 * @returns {Object} - An object containing the language filters and toggle function.
 */
const useLanguageFilters = (initialFilters) => {
  const [languageFilters, setLanguageFilters] = useState(initialFilters);

  /**
   * Toggle the state of a language filter.
   *
   * @param {string} name - The name of the language filter to toggle.
   */
  const handleLanguageFilterToggle = (name) => {
    setLanguageFilters((prevFilters) => {
      const updatedFilters = prevFilters.map((filter) => ({
        ...filter,
        checked: filter.name === name,
      }));

      // Check if at least one filter is checked
      const isAnyFilterChecked = updatedFilters.some((filter) => filter.checked);
      if (!isAnyFilterChecked) {
        // If no filter is checked, set the first filter to be checked
        updatedFilters[0].checked = true;
      }

      return updatedFilters;
    });
  };

  return { languageFilters, handleLanguageFilterToggle };
};

export default useLanguageFilters;

