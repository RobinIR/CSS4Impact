import Head from "next/head";
import { useState, useEffect } from "react";
import FilterPopoverColumns from "../components/FilterPopoverColums";
import DataTable from "../components/DataTable";
import Pagination from "../components/Pagination";
import ErrorDialog from "../components/ErrorDialog";
import useLanguageFilters from "../hooks/useLanguageFilters";
import useCategoryFilters from "../hooks/useCategoryFilters";
import useColumnToggle from "../hooks/useColumnToggle";
import initialLanguageFilters from '../filter/initialLanguageFilters';
import initialColumns from '../filter/initialColumns';



const errorMessageText =
  "Sorry! No valid data available. Try different filters.";

function ArticlesPage() {
  
  // Articles State
  const [articles, setArticles] = useState([]);

  // Loading State
  const [isLoading, setIsLoading] = useState(false);

  const [isErrorDialogOpen, setIsErrorDialogOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const closeErrorDialog = () => {
    setIsErrorDialogOpen(false);
  };

  // Pagination State
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  // Handler, if page changed
  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  // custom hook for language filter
  const { languageFilters, handleLanguageFilterToggle } = useLanguageFilters(
    initialLanguageFilters
  );

  // custom hook for category filter
  const { categoryFilters, handleCategoryFilterToggle, setInitialFilters } = useCategoryFilters(
    /* initialCategoryFilters */[]
  );

  // Priority Filter - no custom hook!
  const [priorityInput, setPriorityInput] = useState("");
  const [maxPriority, setMaxPriority] = useState(0);

  // handler for priority change
  const handlePriorityInputChanged = (text) => {
    setPriorityInput(text);
    setCurrentPage(1);
  };

  // custom hook for columns
  const { columns, handleColumnToggle } = useColumnToggle(initialColumns);


  
  useEffect(() => {
    // effect for only language change 
    const fetchData = async () => {
    
      setIsLoading(true); // State = loading

      const filterArr = languageFilters.filter((item) => item.checked); // get filter for language, one filter needed
     
      // Basic Query Params
      const queryParams = new URLSearchParams({
        Language: filterArr[0].articleProperty, // filter must be set in array item 0
      });

      try {
        // GET max priority for language
        const response = await fetch(`/api/maxPriority?${queryParams}`, { 
          method: "GET",
        });
        const jsonData = await response.json();
        // Set priotity state
        setMaxPriority(jsonData.Priority);

        // GET categorys for language
        const responseObject = await fetch(`/api/categories?${queryParams}`, {
          method: "GET",
        });
        const combinedKeywords = await responseObject.json();

        // set type for UI
        const newCategoryFilters = combinedKeywords.map((keyword) => ({
          name: keyword,
          label: keyword,
          articleProperty: keyword,
          checked: false,
        }));

         // Set filters state
        setInitialFilters(newCategoryFilters);
      } catch (error) {
        if (error.message === errorMessageText) {
          setErrorMessage(error.message);
        } else {
          setErrorMessage("An error occurs: " + error.message);
        }
        setIsErrorDialogOpen(true);
      }
      setIsLoading(false);
    };

    fetchData();
  }, [languageFilters]);



  useEffect(() => {
    // effect for all other changes
    const fetchData = async () => {
    
      setIsLoading(true); // State = loading

      const filterArr = languageFilters.filter((item) => item.checked);
      const filterCategoryArr = categoryFilters.filter((item) => item.checked);
     
      // Basic Query Params
      const queryParams = new URLSearchParams({
        page: currentPage,
        pageSize:  15,
      });

      // Perhaps - Extend Basic Query Params with Language Filter
      if (filterArr.length > 0) {
        queryParams.append("Language", filterArr[0].articleProperty);
      }

      // Perhaps - Extend Basic Query Params with Category Filter
      if (filterCategoryArr.length > 0) {
        const propertyName = "articleProperty";
        const filterValue = filterCategoryArr
          .map((obj) => obj[propertyName])
          .join(" OR ");
        queryParams.append("Category", filterValue);
      }

      // Perhaps - Extend Basic Query Params with Priority Filter
      if (priorityInput != "") {
        queryParams.append("Priority", priorityInput);
      }

      try {
        // GET filtered articles
        const response = await fetch(`/api/articlesData?${queryParams}`, {
          method: "GET",
        });
        const jsonData = await response.json();

        // No articles -> Warning if length = 0
        if (jsonData.records.length === 0) {
          throw new Error(errorMessageText);
        }

        // Set articles state
        setArticles(jsonData.records); //ausprobieren? Ja

        // Set total pages state
        setTotalPages(jsonData.total_pages);
        
      } catch (error) {
        if (error.message === errorMessageText) {
          setErrorMessage(error.message);
        } else {
          setErrorMessage("An error occurs: " + error.message);
        }

        setIsErrorDialogOpen(true);
      }
      setIsLoading(false);
    };

    fetchData();
  }, [languageFilters, categoryFilters, priorityInput, currentPage, columns]);

  // LoadingSpinner!
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="w-16 h-16 relative">
          <div className="h-full flex items-center justify-center">
            <div className="w-8 h-8 bg-blue-600 rounded-full absolute animate-ping"></div>
            <div className="w-8 h-8 bg-blue-600 rounded-full absolute animate-pulse"></div>
          </div>
        </div>
      </div>
    );
  }

  // Page wenn not loading
  return (
    <>
      <Head>
        <title>CSS4IMPACT-ARTICLES</title>
      </Head>

      {/* popup for errors in UI */}
      <main className="px-6 py-4">
        <ErrorDialog
          isOpen={isErrorDialogOpen}
          onClose={closeErrorDialog}
          errorMessage={errorMessage}
        />

        {/* UI */}
        <div className="flex flex-col items-center mb-2">

          {/* function for control */}
          <div className="flex  w-full">
            <div className="flex items-center justify-end w-3/5 ">
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={handlePageChange}
                className="h-full"
              />
            </div>
            <div className="w-1/5"></div>
            <div className=" w-1/5 flex items-center justify-end">
              <FilterPopoverColumns
                label={"Columns"}
                items={columns}
                onChecked={handleColumnToggle}
                className="h-full"
              />
            </div>
          </div>

          {/* data-table */}
          <DataTable
            tableColumns={columns}
            articles={articles}
            handleCategoryFilterToggle={handleCategoryFilterToggle}
            categoryFilters={categoryFilters}
            handleLanguageFilterToggle={handleLanguageFilterToggle}
            languageFilters={languageFilters}
            priorityInput={priorityInput}
            maxPriority={maxPriority}
            handlePriorityInputChanged={handlePriorityInputChanged}
            initPageNumber={() => setCurrentPage(1)}
          />
        </div>
      </main>
    </>
  );
}

export default ArticlesPage;
