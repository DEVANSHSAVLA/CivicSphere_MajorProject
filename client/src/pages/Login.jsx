import React, { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { Shield, Mail, Lock, ArrowRight } from "lucide-react";
import Button from "../components/common/Button";
import Input from "../components/common/Input";
import GoogleSignInButton from "../components/common/GoogleSignInButton";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

export default function Login() {
  const { login } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const from = location.state?.from?.pathname || "/dashboard";

  const validate = () => {
    const errs = {};
    if (!email) {
      errs.email = "Email address is required.";
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      errs.email = "Please enter a valid email address.";
    }
    if (!password) {
      errs.password = "Password is required.";
    } else if (password.length < 6) {
      errs.password = "Password must be at least 6 characters.";
    }
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    try {
      await login(email, password);
      showToast("Welcome back to CivicSphere AI!", "success");
      navigate(from, { replace: true });
    } catch (err) {
      showToast(err.message || "Failed to log in", "error");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F5F8F7] flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-8">
      {/* Centered Login Card */}
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white rounded-2xl border border-[#E5EAE8] py-8 px-6 sm:px-8 shadow-sm">
          
          {/* Header & Logo */}
          <div className="text-center mb-6">
            <Link to="/" className="inline-flex items-center gap-2 mb-4 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#087443] to-[#15965B] flex items-center justify-center shadow-md shadow-[#15965B]/20">
                <Shield className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold tracking-tight text-[#17212B]">
                CivicSphere <span className="text-[#15965B]">AI</span>
              </span>
            </Link>
            <h2 className="text-xl font-extrabold text-[#17212B]">
              Welcome Back!
            </h2>
            <p className="text-xs text-[#64748B] mt-1">
              Login to your account
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Email"
              type="email"
              name="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                if (errors.email) setErrors({ ...errors, email: null });
              }}
              error={errors.email}
              leftIcon={Mail}
              required
            />

            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-xs font-semibold text-[#17212B]">
                  Password <span className="text-red-500">*</span>
                </label>
                <Link
                  to="/forgot-password"
                  className="text-[11px] font-semibold text-[#15965B] hover:text-[#087443] transition"
                >
                  Forgot Password?
                </Link>
              </div>
              <Input
                type="password"
                name="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  if (errors.password) setErrors({ ...errors, password: null });
                }}
                error={errors.password}
                leftIcon={Lock}
                required
              />
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              variant="primary"
              size="md"
              className="w-full font-bold shadow-sm"
              isLoading={isLoading}
            >
              Login
            </Button>
          </form>

          {/* Divider */}
          <div className="relative my-5">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-[#E5EAE8]" />
            </div>
            <div className="relative flex justify-center text-xs">
              <span className="bg-white px-3 text-[#64748B]">or</span>
            </div>
          </div>

          {/* Google Sign In Button */}
          <GoogleSignInButton label="Continue with Google" />

          {/* Footer Link to Sign Up */}
          <p className="mt-6 text-center text-xs text-[#64748B]">
            Don't have an account?{" "}
            <Link
              to="/signup"
              className="font-bold text-[#15965B] hover:text-[#087443] transition"
            >
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

