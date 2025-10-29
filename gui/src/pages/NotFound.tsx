import { Link, useLocation } from "react-router-dom";
import { useEffect } from "react";
import notFoundImage from "@/assets/404.jpeg";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error(
      "404 Error: User attempted to access non-existent route:",
      location.pathname
    );
  }, [location.pathname]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 px-6 py-10">
      <img
        src={notFoundImage}
        alt="Illustration for missing page"
        className="w-full max-w-md rounded-3xl shadow-lg mb-6"
      />
      <h1 className="text-3xl font-semibold text-gray-800 mb-2">Oops! Page not found</h1>
      <p className="text-lg text-gray-600 mb-4">Let&apos;s get you back on track.</p>
      <Link to="/" className="text-blue-500 hover:text-blue-700 underline">
        Return to Home
      </Link>
    </div>
  );
};

export default NotFound;
