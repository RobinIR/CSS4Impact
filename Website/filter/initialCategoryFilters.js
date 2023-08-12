/**
 * Deprecated client-side configuration.
 * Keywords are now fetched from the database.
 */

// An array of combined keywords
const combinedKeywords = [
  "Cash benefits",
  "Provision of food and everyday goods",
  "Provision of accommodation",
  "MedicalCare",
  "Education",
  "Help with finding a job",
  "Childcare",
  "Household help",
  "Help in dealing with the state bureaucracy",
  "Counselling",
  "Criteria for the provision of IDPs with living space",
  "Compact accommodation facility",
  "Long-term settlement of IDPs",
  "Family of IDPs",
  "places of resettlement of IDPs",
  "Employment Promotion",
  "IDP rights",
  "Integration",
  "Reintegration",
  "Status of IDP",
  "IDP status seeker",
  "Granting the status of IDP",
  "Termination of the IDP status",
  "Restoring the status of an IDP",
  "IDP certificate",
  "Social protection of IDPs",
  "State policy towards IDPs",
  "Veteran IDPs",
  "Social rating points",
];

// Generate initial category filters based on combinedKeywords
const initialCategoryFilters = combinedKeywords.map((keyword) => ({
  name: keyword,
  label: keyword,
  articleProperty: keyword,
  checked: false,
}));

export default initialCategoryFilters;
