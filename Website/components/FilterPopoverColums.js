import { Popover } from "@headlessui/react";
import { FilterIcon, ChevronDownIcon } from "@heroicons/react/outline";

/* The component provides a simple and reusable way to render a popover with filter options for columns.
 It allows users to toggle the filters and notifies the parent component through the onChecked prop when a filter is selected or deselected. */

const FilterPopoverColumns = ({ label, items, onChecked }) => {
  console.log("Render FilterPopoverColumns");
  return (
    <div>
      <Popover className="relative">
        <Popover.Button className="inline-flex items-center px-3 py-2 text-base font-medium text-white bg-blue-500 rounded-md group hover:text-opacity-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 hover:bg-blue-600 hover:scale-105 transform transition-all">
          {label}
          <ChevronDownIcon className="w-5 h-5 ml-2 text-white" />
        </Popover.Button>
        <Popover.Panel className="absolute z-10 mt-3 bg-gray-100 rounded-md right-2">
          <div className="grid gap-4 p-4">
            {items.map((item) => (
              <label key={item.name} className="flex items-center">
                <input
                  type="checkbox"
                  checked={item.checked}
                  onChange={() => onChecked(item.name)}
                  className="mr-2"
                />
                <span className="text-sm">{item.label}</span>
              </label>
            ))}
          </div>
        </Popover.Panel>
      </Popover>
    </div>
  );
};

export default FilterPopoverColumns;
