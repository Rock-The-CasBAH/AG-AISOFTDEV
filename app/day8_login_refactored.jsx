import React from 'react';

// Sub-component for input fields with label
function InputWithIcon({ type, id, name, placeholder, label }) {
  return (
    <div className="mb-4">
      <label
        htmlFor={id}
        className="block text-gray-700 text-sm font-bold mb-2"
      >
        {label}
      </label>
      <input
        type={type}
        id={id}
        name={name}
        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        placeholder={placeholder}
      />
    </div>
  );
}

// Sub-component for the login button
function LoginButton({ children }) {
  return (
    <button
      type="submit"
      className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
    >
      {children}
    </button>
  );
}

// Main LoginForm component
function LoginForm() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
        <form>
          <InputWithIcon
            type="email"
            id="email"
            name="email"
            placeholder="Enter your email"
            label="Email"
          />
          <InputWithIcon
            type="password"
            id="password"
            name="password"
            placeholder="Enter your password"
            label="Password"
          />
          <div className="flex items-center justify-between">
            <LoginButton>Sign In</LoginButton>
            <a
              className="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800"
              href="#"
            >
              Forgot Password?
            </a>
          </div>
        </form>
      </div>
    </div>
  );
}

export default LoginForm;