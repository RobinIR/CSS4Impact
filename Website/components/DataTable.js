import FilterPopoverRows from "../components/FilterPopoverRows";
import FilterTextFieldPopoverRows from "./FilterTextfieldPopoverRows";
import KeywordsColumn from "./KeywordsColumn";
import URLViewer from "./URLViewer";
import CopyOnClick from "./CopyOnClick";

/* the DataTable component renders a dynamic table based on the provided columns and articles data.
    It generates the table header cells based on the column names, with specific functionality for certain columns.
    It also generates the table cells based on the checked columns and renders the appropriate content for each cell. */

const renderTd = (article, column) => {
  if (column.name === "location") {
    return (
      <td key={column.name} className="px-4 py-2 border">
        <KeywordsColumn
          label={column.label}
          keywords={article[column.articleProperty]}
        />
      </td>
    );
  } else if (column.name === "actors") {
    return (
      <td key={column.name} className="px-4 py-2 border">
        <KeywordsColumn
          label={column.label}
          keywords={article[column.articleProperty]}
        />
      </td>
    );
  } else if (column.name === "organisations") {
    return (
      <td key={column.name} className="px-4 py-2 border">
        <KeywordsColumn
          label={column.label}
          keywords={article[column.articleProperty]}
        />
      </td>
    );
  } else if (column.name === "keywords") {
    return (
      <td key={column.name} className="px-4 py-2 border">
        <KeywordsColumn
          label={column.label}
          keywords={article[column.articleProperty]}
        />
      </td>
    );
  } else if (column.name === "IDPMatchedKeywords") {
    return (
      <td key={column.name} className="px-4 py-2 border">
        <KeywordsColumn
          label={column.label}
          keywords={article[column.articleProperty]}
        />
      </td>
    );
  } else if (column.name === "categoryMatchedKeywords") {
    return (
      <td key={column.name} className="px-4 py-2 border">
        <KeywordsColumn
          label={column.label}
          keywords={article[column.articleProperty]}
        />
      </td>
    );
  } else if (column.name === "local-path") {
    return (
      <td key={column.name} className="px-4 py-2 border">
        <CopyOnClick filePath={article[column.articleProperty]} />
      </td>
    );
  } else if (column.name === "url") {
    return (
      <td key={column.name} className="px-4 py-2 border">
        <URLViewer url={article[column.articleProperty]} />
      </td>
    );
  }
  return (
    <td key={column.name} className="px-4 py-2 border">
      {article[column.articleProperty]}
    </td>
  );
};

const DataTable = ({
  tableColumns,
  articles,
  handleLanguageFilterToggle,
  languageFilters,
  handleCategoryFilterToggle,
  categoryFilters,
  priorityInput,
  maxPriority,
  handlePriorityInputChanged,
  initPageNumber,
}) => {
  const ColumnHeader = ({ column }) => {
    if (column.name === "language") {
      return (
        <th className="bg-gray-200">
          <div className="flex items-center px-2">
            <FilterPopoverRows
              label={column.label}
              items={languageFilters}
              handleFilterToggle={handleLanguageFilterToggle}
              initPageNumber={initPageNumber}
              className="h-full"
            />
          </div>
        </th>
      );
    } else if (column.name === "category") {
      return (
        <th className="bg-gray-200">
          <div className="flex items-center px-2">
            <FilterPopoverRows
              label={column.label}
              items={categoryFilters}
              handleFilterToggle={handleCategoryFilterToggle}
              initPageNumber={initPageNumber}
              className="h-full"
            />
          </div>
        </th>
      );
    } else if (column.name === "priority") {
      return (
        <th className="bg-gray-200">
          <div className="flex items-center px-2">
            <FilterTextFieldPopoverRows
              label={column.label}
              text={priorityInput}
              maxValue={maxPriority}
              onChanged={handlePriorityInputChanged}
              initPageNumber={initPageNumber}
              className="h-full"
            />
          </div>
        </th>
      );
    }

    return (
      <th className="bg-gray-200">
        <div className="flex items-center px-2">
          <span className="mr-1">{column.label}</span>
        </div>
      </th>
    );
  };

  return (
    <table className="w-full mb-4 overflow-y-auto max-h-96">
      <thead>
        <tr>
          {tableColumns.map((column) => {
            if (column.checked) {
              return <ColumnHeader key={column.name} column={column} />;
            } else {
              return null;
            }
          })}
        </tr>
      </thead>
      <tbody>
        {articles?.map((article) => {
          return (
            <tr key={article.id}>
              {tableColumns.map((column) => {
                if (column.checked) {
                  return renderTd(article, column);
                } else {
                  return null;
                }
              })}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export default DataTable;
