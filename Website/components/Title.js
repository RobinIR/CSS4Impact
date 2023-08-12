/**
 * The Title component displays a styled title with a background color.
 *
 * @param {string} label - The text to be displayed as the title.
 * @returns {JSX.Element} The Title component.
 */
function Title({ label }) {
  return (
    <p className='inline-flex items-center px-3 py-2 text-base font-medium text-white bg-blue-500 rounded-md group hover:text-opacity-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75'>
      {label}
    </p>
  );
}

export default Title;
