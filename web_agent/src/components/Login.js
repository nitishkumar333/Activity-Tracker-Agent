import { useState } from "react";
import "./login.css";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "./firebase";
import { toast } from "react-toastify";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const loginHandler = async (e) => {
    e.preventDefault();
    try {
      await signInWithEmailAndPassword(auth, email, password);
      console.log("User logged in Successfully");
      window.location.href = "/profile";
      toast.success("User logged in Successfully", {
        position: "top-center",
      });
    } catch (error) {
      console.log(error.message);

      toast.error(error.message, {
        position: "bottom-center",
      });
    }
  };

  return (
    <div className="outerbox">
      <div className="innerbox">
        <header className="signup-header">
          <h1>Login User</h1>
        </header>
        <main className="signup-body">
          <form onSubmit={loginHandler}>
            <p>
              <label htmlFor="email">Username :</label>
              <input
                type="email"
                id="email"
                placeholder="Enter Your Username"
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="off"
              />
            </p>
            <p>
              <label htmlFor="password">Password :</label>
              <input
                type="password"
                id="password"
                placeholder="Enter Your Password"
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="off"
              />
            </p>
            <p>
              <input type="submit" id="submit" value="Login" />
            </p>
          </form>
        </main>
      </div>
    </div>
  );
};

export default Login;
