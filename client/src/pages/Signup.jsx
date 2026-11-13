import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Shield, User, Mail, Lock } from "lucide-react";
import Button from "../components/common/Button";
import Input from "../components/common/Input";
import GoogleSignInButton from "../components/common/GoogleSignInButton";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

export default function Signup() {
  const { signup } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    agreeTerms: false,
  });

  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const validate = () => {
    const errs = {};
    if (!formData.name.trim()) {
      errs.name = "Full name is required.";
    }
    if (!formData.email.trim()) {
      errs.email = "Email address is required.";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errs.email = "Please enter a valid email address.";
    }
    if (!formData.password) {
      errs.password = "Password is required.";
    } else if (formData.password.length < 6) {
      errs.password = "Password must be at least 6 characters.";
    }
    if (formData.password !== formData.confirmPassword) {
      errs.confirmPassword = "Passwords do not match.";
    }
    if (!formData.agreeTerms) {
      errs.agreeTerms = "You must agree to the Terms & Conditions.";
    }
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    try {
      await signup(formData);
      showToast("Account created successfully! Welcome to CivicSphere AI.", "success");
      navigate("/dashboard");
    } catch (err) {
      showToast(err.message || "Failed to create account", "error");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F5F8F7] flex flex-col justify-center py-10 px-4 sm:px-6 lg:px-8">
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
              Create Account
            </h2>
            <p className="text-xs text-[#64748B] mt-1">
              Join CivicSphere AI today
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-3.5">
            <Input
              label="Full Name"
              type="text"
              placeholder="Enter your full name"
              value={formData.name}
              onChange={(e) => {
                setFormData({ ...formData, name: e.target.value });
                if (errors.name) setErrors({ ...errors, name: null });
              }}
              error={errors.name}
              leftIcon={User}
              required
            />

            <Input
              label="Email"
              type="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={(e) => {
                setFormData({ ...formData, email: e.target.value });
                if (errors.email) setErrors({ ...errors, email: null });
              }}
              error={errors.email}
              leftIcon={Mail}
              required
            />

            <Input
              label="Password"
              type="password"
              placeholder="Create a password"
              value={formData.password}
              onChange={(e) => {
                setFormData({ ...formData, password: e.target.value });
                if (errors.password) setErrors({ ...errors, password: null });
              }}
              error={errors.password}
              leftIcon={Lock}
              required
            />

            <Input
              label="Confirm Password"
              type="password"
              placeholder="Confirm your password"
              value={formData.confirmPassword}
              onChange={(e) => {
                setFormData({ ...formData, confirmPassword: e.target.value });
                if (errors.confirmPassword)
                  setErrors({ ...errors, confirmPassword: null });
              }}
              error={errors.confirmPassword}
              leftIcon={Lock}
              required
            />

            {/* Terms checkbox */}
            <div>
              <div className="flex items-start">
                <input
                  id="agree-terms"
                  type="checkbox"
                  checked={formData.agreeTerms}
                  onChange={(e) => {
                    setFormData({ ...formData, agreeTerms: e.target.checked });
                    if (errors.agreeTerms)
                      setErrors({ ...errors, agreeTerms: null });
                  }}
                  className="h-4 w-4 rounded border-[#E5EAE8] text-[#15965B] focus:ring-[#15965B] mt-0.5"
                />
                <label
                  htmlFor="agree-terms"
                  className="ml-2 block text-xs text-[#64748B] select-none cursor-pointer"
                >
                  I agree to the{" "}
                  <span className="text-[#15965B] font-semibold hover:underline">
                    Terms & Conditions
                  </span>{" "}
                  and{" "}
                  <span className="text-[#15965B] font-semibold hover:underline">
                    Privacy Policy
                  </span>
                </label>
              </div>
              {errors.agreeTerms && (
                <p className="mt-1 text-xs text-red-500 font-medium">
                  {errors.agreeTerms}
                </p>
              )}
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              variant="primary"
              size="md"
              className="w-full font-bold shadow-sm mt-2"
              isLoading={isLoading}
            >
              Sign Up
            </Button>
          </form>

          {/* Divider */}
          <div className="relative my-4">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-[#E5EAE8]" />
            </div>
            <div className="relative flex justify-center text-xs">
              <span className="bg-white px-3 text-[#64748B]">or</span>
            </div>
          </div>

          {/* Continue with Google */}
          <GoogleSignInButton label="Register with Google" />

          {/* Footer Link */}
          <p className="mt-5 text-center text-xs text-[#64748B]">
            Already have an account?{" "}
            <Link
              to="/login"
              className="font-bold text-[#15965B] hover:text-[#087443] transition"
            >
              Login
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

