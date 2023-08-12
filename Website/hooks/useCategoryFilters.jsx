import { useState } from "react";

/**
 * Custom hook for managing category filters.
 * This hook provides functionality to manage category filters,
 * including setting initial filters, toggling filter states,
 * and accessing the current category filters.
 *
 * @param {Array} initialFilters - The initial category filters.
 * @returns {Object} - An object containing the category filters, filter toggle function, and set initial filters function.
 */
const useCategoryFilters = (initialFilters) => {
  const [categoryFilters, setCategoryFilters] = useState(initialFilters);

  /**
   * Set the initial category filters.
   *
   * @param {Array} newFilters - The new category filters.
   */
  const setInitialFilters = (newFilters) => {
    setCategoryFilters(newFilters);
  };

  /**
   * Toggle the state of a category filter.
   *
   * @param {string} name - The name of the category filter to toggle.
   */
  const handleCategoryFilterToggle = (name) => {
    setCategoryFilters((prevItems) => {
      const updatedFilters = prevItems.map((item) => ({
        ...item,
        checked: item.name === name && !item.checked,
      }));
      return updatedFilters;
    });
  };

  return { categoryFilters, handleCategoryFilterToggle, setInitialFilters };
};

export default useCategoryFilters;
