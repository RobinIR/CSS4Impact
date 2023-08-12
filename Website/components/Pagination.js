/**
 * The Pagination component displays a pagination control with previous and next buttons,
 * along with the current page and total pages information. It also allows for custom content
 * to be included within the pagination section.
 */
const Pagination = ({ currentPage, totalPages, onPageChange, children }) => {
  /**
   * Handles the previous page button click event.
   * Calls the onPageChange function with the previous page number.
   */
  const handlePreviousPage = () => {
    if (currentPage > 1) {
      onPageChange(currentPage - 1);
    }
  };

  /**
   * Handles the next page button click event.
   * Calls the onPageChange function with the next page number.
   */
  const handleNextPage = () => {
    if (currentPage < totalPages) {
      onPageChange(currentPage + 1);
    }
  };

  return (
    <div>
      {/* Pagination Section */}
      <div className="flex justify-center p-4 my-4">
        {/* Previous Page Button */}
        <button
          onClick={handlePreviousPage}
          disabled={currentPage === 1}
          className="w-24 px-4 py-2 text-white bg-blue-500 rounded disabled:bg-gray-300 disabled:text-gray-500 hover:bg-blue-600 hover:scale-105 transform transition-all"
        >
          Previous
        </button>

        {/* Current Page Indicator */}
        <span className="flex items-center justify-center w-24 border-l border-r">
          {currentPage} / {totalPages}
        </span>

        {/* Next Page Button */}
        <button
          onClick={handleNextPage}
          disabled={currentPage === totalPages}
          className="w-24 mr-8 px-4 py-2 text-white bg-blue-500 rounded disabled:bg-gray-300 disabled:text-gray-500 hover:bg-blue-600 hover:scale-105 transform transition-all"
        >
          Next
        </button>

        {/* Custom Content */}
        {children}
      </div>
    </div>
  );
};

export default Pagination;
