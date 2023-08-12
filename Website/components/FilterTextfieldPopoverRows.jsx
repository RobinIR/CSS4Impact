import { Popover } from "@headlessui/react";
import { ChevronDownIcon } from "@heroicons/react/outline";
import { useState } from "react";

/* The component provides a way to render a popover with a text input field for filtering rows based on a numerical value.
 Users can enter a value, reset the filter, or set the filter value.
  The onChanged and initPageNumber functions are invoked to handle the filter change and reset the page number accordingly. */

const FilterTextfieldPopoverRows = ({ label, text, maxValue, onChanged, initPageNumber}) => {
  const [number, setNumber] = useState(text);

  const handleNumberInput = (event) => {
    const inputValue = event.target.value;
    const regex = /^\d+(\.\d{0,1})?$/;

    if (regex.test(inputValue)) {
      setNumber(inputValue);
    } else if (inputValue === "") {
      setNumber("");
    }
  };

  const condition = text !== "";

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
          <span className={`mr-2 ${condition ? "text-white" : "text-black"}`}>
            {label}
          </span>
          <ChevronDownIcon
            className={`w-5 h-5 ${condition ? "text-white" : "text-black"}`}
          />
        </Popover.Button>
        <Popover.Panel className="absolute z-10 mt-3 bg-gray-100 rounded-md right-2">
          <div className="grid gap-2 p-4">

            

            <div>
              <input placeholder={maxValue} type="number" value={number} max={maxValue} onChange={handleNumberInput}/>
              <p className="text-sm text-gray-500">Highest available priority: {maxValue}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <button
                className={`inline-flex items-center px-3 py-2 text-base font-medium rounded-md group focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 transform transition-all ${
                  condition
                    ? "bg-blue-500 hover:bg-blue-600"
                    : "bg-gray-200 hover:bg-gray-300"
                }`}
                onClick={() => {onChanged(""); initPageNumber();}}
              >
                <span
                  className={`mr-2 ${condition ? "text-white" : "text-black"}`}
                >
                  Reset
                </span>
              </button>
              <button
                className={`inline-flex items-center px-2 py-2 text-base font-medium rounded-md group focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 transform transition-all ${
                  condition
                    ? "bg-gray-200 hover:bg-gray-300"
                    : "bg-blue-500 hover:bg-blue-600"
                }`}
                onClick={() => {onChanged(number); initPageNumber()}}
              >
                <span
                  className={`mr-2 ${condition ? "text-black" : "text-white"}`}
                >
                  Set
                </span>
              </button>
            </div>
          </div>
        </Popover.Panel>
      </Popover>
    </div>
  );
};

export default FilterTextfieldPopoverRows;
