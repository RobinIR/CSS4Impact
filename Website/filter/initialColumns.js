/**
 * Columns Selection client-side configuration.
 * This code defines the initial columns for selection in a table.
 */
const initialColumns = [
    { name: "title", label: "Title", articleProperty: "title", checked: true },
    {
      name: "date-publication",
      label: "Date Publication",
      articleProperty: "DatePublication",
      checked: true,
    },
    {
      name: "language",
      label: "Language",
      articleProperty: "Language",
      checked: true,
    },
    {
      name: "priority",
      label: "Priority",
      articleProperty: "Priority",
      checked: true,
    },
    {
      name: "url",
      label: "Url",
      articleProperty: "Url",
      checked: true,
    },
    {
      name: "actors",
      label: "Actors",
      articleProperty: "Actors",
      checked: true,
    },

    {
      name: "organisations",
      label: "Organisations",
      articleProperty: "Organizations",
      checked: true,
    },
    {
      name: "IDPMatchedKeywords",
      label: "IDP Matched Keywords",
      articleProperty: "IDPMatchedKeywords",
      checked: false,
    },

    {
      name: "category",
      label: "Category",
      articleProperty: "Category",
      checked: true,
    },

    {
      name: "categoryMatchedKeywords",
      label: "Category Matched Keywords",
      articleProperty: "CatagoryMatchedKeywords",
      checked: false,
    },
    {
      name: "keywords",
      label: "Keywords",
      articleProperty: "KeyWords",
      checked: true,
    },
    {
      name: "local-path",
      label: "Local Path",
      articleProperty: "LocalPath",
      checked: false,
    },
  ];

  export default initialColumns;