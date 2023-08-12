import Head from "next/head";
import { useSpring, animated } from "react-spring";

/**
 * The HomePage component that displays the home page content.
 *
 * @returns {JSX.Element} - The rendered HomePage component.
 */

const HomePage = () => {
  const animationProps = useSpring({
    from: { opacity: 0, letterSpacing: "-0.5em" },
    to: { opacity: 1, letterSpacing: "0em" },
    config: { duration: 2000 },
  });

  return (
    <>
      <Head>
        <title>CSS4IMPACT</title>
      </Head>

      <main>
        <div className="flex justify-center items-center h-screen">
          <animated.h1
            className="text-7xl font-bold text-center text-blue-500"
            style={animationProps}
          >
            WELCOME TO CSS4IMPACT
          </animated.h1>
        </div>
      </main>
    </>
  );
};

export default HomePage;
