import { Popover } from "@headlessui/react";
import { FilterIcon, ChevronDownIcon } from "@heroicons/react/outline";

/* The component provides a way to render a popover with filter options for rows.
 It allows users to toggle the filters and notifies the parent component through the handleFilterToggle prop when a filter is selected or deselected.
  Additionally, it includes the initPageNumber function that can be called to reset the page number when a filter is applied or removed. */

const FilterPopoverRows = ({ label, items, handleFilterToggle, initPageNumber }) => {
  console.log("Render FilterPopoverRows");

  const arr = items.filter((item) => item.checked);
  const condition = arr.length > 0;
  return (
    <div>
      <Popover className="relative">
        <Popover.Button
          className={`inline-flex items-center px-3 py-2 text-base font-medium rounded-md group focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 transform transition-all ${
            condition
              ? "bg-blue-500 hover:bg-blue-600"
              : "bg-gray-200 hover:bg-gray-300"
          }`}
        >
          <span
            className={`mr-2 ${
              condition ? "text-white" : "text-black"
            }`}
          >
            {label}
          </span>
          <ChevronDownIcon
            className={`w-5 h-5 ${
              condition ? "text-white" : "text-black"
            }`}
          />
        </Popover.Button>
        <Popover.Panel className="fixed z-10 mt-3 mr-5 bg-gray-100 rounded-md right-2 w-96 h-80 overflow-y-auto">
          <div className="grid gap-2 p-4">
            {items.map((item) => (
              <label key={item.name} className="flex items-center">
                <input
                  type="checkbox"
                  checked={item.checked}
                  onChange={() => {handleFilterToggle(item.name); initPageNumber();}}
                  className="mr-2"
                />
                <span className="text-xs">{item.label}</span>
              </label>
            ))}
          </div>
        </Popover.Panel>
      </Popover>
    </div>
  );
};

export default FilterPopoverRows;

