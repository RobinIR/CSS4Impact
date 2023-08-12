import { Popover } from '@headlessui/react';
import { FilterIcon } from '@heroicons/react/outline';

/* FilterPopover component provides a flexible and reusable way to render a popover with filter options based on the provided columns and selectedColumns props.
 It allows users to toggle filters and notifies the parent component through the onChecked prop when a filter is selected or deselected. */

const FilterPopover = ({columns, selectedColumns, onChecked}) => {
  console.log("Render FilterPopover")
  return (
    <div className="fixed top-20 right-6">
      <Popover className="relative">
        <Popover.Button
          className="group inline-flex items-center rounded-md bg-blue-700 px-3 py-2 text-base font-medium text-white hover:text-opacity-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75"
        >
          <FilterIcon className="h-5 w-5 text-white mr-2" />
          Filters
        </Popover.Button>
        <Popover.Panel className="absolute z-10 mt-3 bg-gray-100 rounded-md right-2">
          <div className="grid gap-4 p-7">
            {columns.map((column) => (
                <label key={column.name}>
                <input
                    type="checkbox"
                    checked={selectedColumns.some((selected) => selected.name === column.name)}
                    onChange={() => onChecked(column.name)}
                />
                {column.label}
                </label>
            ))}
        </div>

        </Popover.Panel>
      </Popover>
    </div>

  );
}


export default FilterPopover;


