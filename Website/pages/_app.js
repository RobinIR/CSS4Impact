import Head from "next/head";
import { GoogleFonts } from "next-google-fonts";
import NavbarTailwind from "../components/NavbarTailwind";
import "../styles/globals.css";

/**
 * The main App component that wraps the entire application.
 *
 * @param {object} props - The component props.
 * @returns {JSX.Element} - The rendered App component.
 */
function App({ Component, pageProps }) {
  return (
    <>
      <Head>
        <link rel="icon" href="/icons/favicon.ico" />
        <GoogleFonts href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500;700&display=swap" />
      </Head>
      <header className="sticky top-0 z-10">
        <NavbarTailwind />
      </header>
      <Component {...pageProps} />
    </>
  );
}

export default App;
