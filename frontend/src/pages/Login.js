import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import { handleError, handleSuccess } from "../utils";
import bgImage from "../assets/background.png";

function Login() {
  const [loginInfo, setLoginInfo] = useState({ email: "", password: "" });
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setLoginInfo((prev) => ({ ...prev, [name]: value }));
  };

  const handleLogin = async (e) => {
  e.preventDefault();
  const { email, password } = loginInfo;
  if (!email || !password) {
    return handleError("Email and password are required");
  }
  try {
    const response = await fetch("http://localhost:4000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(loginInfo),
    });
    const result = await response.json();
    const { success, message, jwtToken, name, userId, error } = result;
    if (success) {
      handleSuccess(message);
      localStorage.setItem("token", jwtToken);
      localStorage.setItem("loggedInUser", name);
      localStorage.setItem("userId", userId);
      setTimeout(() => navigate("/chatpage"), 1000);
    } else {
      handleError(error?.details[0]?.message || message);
    }
  } catch (err) {
    handleError(err.message);
  }
};


  return (
    <div className="min-h-screen flex flex-col md:flex-row">
      {/* Left: Login Form */}
      <div className="w-full md:w-1/2 flex items-center justify-center bg-black px-8 py-12">
        <div className="w-full max-w-md space-y-6">
          <h1 className="text-4xl font-bold text-white mb-4 tracking-tight">
            Welcome to <span className="text-green-400">Vaanika.AI</span>
          </h1>
          <p className="text-zinc-400 mb-6">Sign in to your dashboard</p>

          <form onSubmit={handleLogin} className="space-y-5">
            <div>
              <label
                htmlFor="email"
                className="block mb-2 text-sm text-zinc-300"
              >
                Email
              </label>
              <input
                type="email"
                name="email"
                placeholder="you@example.com"
                value={loginInfo.email}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-zinc-900 border border-zinc-700 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="block mb-2 text-sm text-zinc-300"
              >
                Password
              </label>
              <input
                type="password"
                name="password"
                placeholder="••••••••"
                value={loginInfo.password}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-zinc-900 border border-zinc-700 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>

            <button
              type="submit"
              className="w-full py-3 bg-green-500 hover:bg-green-600 transition rounded-xl font-semibold text-black"
            >
              Sign In
            </button>
          </form>

          <p className="text-sm text-zinc-500 mt-4">
            Don’t have an account?
            <Link to="/signup" className="text-green-400 hover:underline ml-1">
              Sign up
            </Link>
          </p>
        </div>
      </div>

      {/* Right: Image / Texture Section */}
      <div
        className="hidden md:block w-full md:w-1/2 bg-cover bg-center relative"
        style={{ backgroundImage: `url(${bgImage})` }}
      >
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center px-6">
            <h2 className="text-5xl font-extrabold text-white drop-shadow-lg">
              KalaaSetu
            </h2>
            <p className="mt-4 text-zinc-300 text-lg max-w-md mx-auto">
              AI studio that empowers creators to create and narrate stories that inspire.
            </p>
          </div>
        </div>
      </div>

      <ToastContainer />
    </div>
  );
}

export default Login;
