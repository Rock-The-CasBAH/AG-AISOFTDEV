import React, { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log({ email, password, remember });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-50 via-white to-indigo-50 flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        <div className="bg-white/95 backdrop-blur-sm shadow-xl rounded-2xl overflow-hidden">
          <div className="p-8 sm:p-10">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-12 bg-indigo-600 rounded-lg flex items-center justify-center">
                <svg className="w-7 h-7 text-white" viewBox="0 0 24 24" fill="none" aria-hidden>
                  <path d="M12 2L20 7v6c0 5-4 9-8 9s-8-4-8-9V7l8-5z" stroke="currentColor" strokeWidth="0" fill="currentColor" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-semibold text-gray-800">Welcome back</h1>
                <p className="text-sm text-gray-500">Sign in to continue to your account</p>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5" aria-label="Login form">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3 rounded-lg border border-gray-200 bg-white text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:border-indigo-300"
                  placeholder="you@example.com"
                  aria-required="true"
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                  Password
                </label>
                <div className="relative">
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? "text" : "password"}
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full px-4 py-3 rounded-lg border border-gray-200 bg-white text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:border-indigo-300 pr-12"
                    placeholder="Enter your password"
                    aria-required="true"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword((s) => !s)}
                    aria-pressed={showPassword}
                    aria-label={showPassword ? "Hide password" : "Show password"}
                    className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-md text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-300"
                  >
                    {showPassword ? (
                      <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" aria-hidden>
                        <path d="M3 3l18 18" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M9.88 9.88A3 3 0 0114.12 14.12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M10.7 5.1C12.1 4.7 13.5 4.5 15 4.5c4 0 7 3.5 7 7.5 0 1.1-.25 2.2-.7 3.2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M6.2 6.8C4.8 8 4 9.6 4 11.5 4 13.5 6.5 17 12 17c1.1 0 2.2-.1 3.2-.4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                    ) : (
                      <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" aria-hidden>
                        <path d="M12 5c-4 0-7 3.5-7 7.5S8 20 12 20s7-3.5 7-7.5S16 5 12 5z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M12 9.5a3.5 3.5 0 100 7 3.5 3.5 0 000-7z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                    )}
                  </button>
                </div>
              </div>

              <div className="flex items-center justify-between text-sm text-gray-600">
                <label className="inline-flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={remember}
                    onChange={(e) => setRemember(e.target.checked)}
                    className="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-300"
                    aria-label="Remember me"
                  />
                  <span>Remember me</span>
                </label>
                <a href="#" className="text-indigo-600 hover:underline">
                  Forgot password?
                </a>
              </div>

              <div>
                <button
                  type="submit"
                  className="w-full inline-flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-indigo-600 to-indigo-500 text-white font-medium rounded-lg shadow hover:from-indigo-700 hover:to-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-300"
                >
                  Sign in
                </button>
              </div>
            </form>

            <div className="mt-6 text-center text-sm text-gray-500">
              <span>New here? </span>
              <a href="#" className="text-indigo-600 hover:underline">
                Create an account
              </a>
            </div>
          </div>

          <div className="hidden sm:block bg-gradient-to-r from-indigo-50 to-white px-8 py-6 border-t border-gray-100">
            <div className="text-xs text-gray-500 text-center">Secure sign in • Protected by best practices</div>
          </div>
        </div>
      </div>
    </div>
  );
}
