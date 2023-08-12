import path from "path";

/* This component is responsible for rendering a button with an icon representing a file.
 When the button is clicked, it opens a new window with the file's URL. */

 //It's important to note that this component is defined but not currently being used or rendered in any other component.

 // ----------------
/*  Utilizing the FileViewer component in Next.js allows you to incorporate file viewing and interaction capabilities seamlessly into your application 
    while taking advantage of Next.js's server-side rendering, dynamic routing, and extensibility. */
 //It's important to note that directly accessing files from a user's device without their consent or knowledge would be a violation of their privacy and a potential security risk.
 //Therefore, web browsers impose restrictions to ensure that user data remains secure and private.

const hexColor = "#4676FB";

const FileViewer = ({ filePath }) => {
  const openNewWindow = async () => {
    const fileName = path.basename(filePath);

    const fileUrl = path.join("txt-files", fileName);
    console.log("fileUrl= ", fileUrl);
    window.open(fileUrl, "TXT-Window");
  };

  return (
    <div>
      <button onClick={openNewWindow}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke={hexColor}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="feather feather-file"
        >
          <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path>
          <polyline points="13 2 13 9 20 9"></polyline>
        </svg>
      </button>
    </div>
  );
};

export default FileViewer;
