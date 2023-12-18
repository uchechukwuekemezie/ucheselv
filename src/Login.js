import React from "react";
import { Link } from "react-router-dom";

class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      emailOrPhone: "",
      password: "",
      errors: {
        emailOrPhone: "",
        password: "",
      },
    };
  }

  handleInputChange = (e) => {
    const { name, value } = e.target;
    this.setState({
      [name]: value,
    });
  };

  validateForm = () => {
    const { emailOrPhone, password } = this.state;
    let errors = {
      emailOrPhone: "",
      password: "",
    };

    // Validate Email/Phone
    const emailOrPhoneRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailOrPhoneRegex.test(emailOrPhone)) {
      errors.emailOrPhone = "Invalid email or phone format";
    }

    // Validate Password (at least 8 characters)
    if (password.length < 8) {
      errors.password = "Password must be at least 8 characters";
    }

    // Update the state with errors
    this.setState({ errors });

    // Return true if there are no errors
    return Object.values(errors).every((error) => error === "");
  };

  handleSubmit = (e) => {
    e.preventDefault();

    if (this.validateForm()) {
      // Add your login logic here using this.state
      console.log("Form submitted with data:", this.state);
    } else {
      // Form validation failed, handle errors in the UI
      console.log("Form validation failed");
    }
  };

  render() {
    const { errors } = this.state;

    return (
      <div>
        <h2>Login</h2>
        <form onSubmit={this.handleSubmit}>
          <div>
            <label>Email or Phone:</label>
            <input
              type="text"
              name="emailOrPhone"
              value={this.state.emailOrPhone}
              onChange={this.handleInputChange}
              placeholder="Enter your email or phone"
            />
            {errors.emailOrPhone && (
              <span className="error">{errors.emailOrPhone}</span>
            )}
          </div>
          <div>
            <label>Password:</label>
            <input
              type="password"
              name="password"
              value={this.state.password}
              onChange={this.handleInputChange}
              placeholder="Enter your password"
            />
            {errors.password && (
              <span className="error">{errors.password}</span>
            )}
          </div>
          <div>
            <button type="submit">Login</button>
          </div>
          <div>
            <p>
              Don't have an account?
              <Link to="/src/Signup.js">Sign up here.</Link>
            </p>
          </div>
        </form>
      </div>
    );
  }
}

export default Login;
