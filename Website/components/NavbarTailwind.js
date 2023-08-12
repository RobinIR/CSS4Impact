import Link from "next/link";
import Image from "next/image";
import { useState } from "react";
import PDFViewer from "./PDFViewer";

/**
 * The NavbarTailwind component represents the navigation bar of the web application.
 * It provides links to different pages and includes a responsive menu for mobile devices.
 */


const NavbarTailwind = () => {
  const [active, setActive] = useState(false);

  const handleClick = () => {
    setActive(!active);
  };

  return (
    <div>
      {/* Navigation Bar */}
      <nav className="flex flex-wrap items-center p-1 bg-[#4676FB]">
        {/* Logo */}
        <Link
          className="inline-flex items-center p-1 m-1 "
          href="/"
        >
          <Image width={85} height={85} src="/img/Logo.png" alt="Logo" priority="true" />
        </Link>
        <button
          className="inline-flex p-3 ml-auto text-white rounded outline-none hover:hover:bg-blue-700 lg:hidden hover:text-white"
          onClick={handleClick}
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
        </button>
        {/* Navigation Links */}
        <div
          className={`${
            active ? "" : "hidden"
          } w-full lg:inline-flex lg:flex-grow lg:w-auto`}
        >
          <div className="flex flex-col items-start w-full lg:inline-flex lg:flex-row lg:ml-auto lg:w-auto lg:items-center lg:h-auto">
            <Link
              className="items-center justify-center w-full px-3 py-2 font-bold text-white rounded lg:inline-flex lg:w-auto  hover:bg-blue-700 hover:animate-pulse"
              href="/"
            >
              Home
            </Link>

            <Link
              className="items-center justify-center w-full px-3 py-2 font-bold text-white rounded lg:inline-flex lg:w-auto hover:bg-blue-700 hover:animate-pulse"
              href="/articles"
            >
              Articles
            </Link>
            <Link
              className="items-center justify-center w-full px-3 py-2 font-bold text-white rounded lg:inline-flex lg:w-auto hover:bg-blue-700 hover:animate-pulse"
              href="/about"
            >
              About
            </Link>
            {/* PDF Viewer for UserManuel */}
            <div className="mx-8 mt-1">
            <PDFViewer/>
            </div>
          </div>
        </div>
      </nav>
    </div>
  );
};

export default NavbarTailwind;
