import { React } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";

export default function NavBarBuyer() {
    let navigate = useNavigate();
    let location = useLocation();

    const handleLogout = () => {
        localStorage.removeItem("auth-token");
        navigate("/home");
    };

    return (
        <div>
            {localStorage.getItem("auth-token") && (
                <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                    <div className="container-fluid">
                        <Link className="navbar-brand" to="/">
                            vCart
                        </Link>
                        <button
                            className="navbar-toggler"
                            type="button"
                            data-bs-toggle="collapse"
                            data-bs-target="#navbarSupportedContent"
                            aria-controls="navbarSupportedContent"
                            aria-expanded="false"
                            aria-label="Toggle navigation"
                        >
                            <span className="navbar-toggler-icon"></span>
                        </button>
                        <div className="collapse navbar-collapse" id="navbarSupportedContent">
                            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                                <li className="nav-item">
                                    <Link className={`nav-link ${location.pathname === "/buyer" ? "active" : ""}`} to="/buyer">
                                        Buyer
                                    </Link>
                                </li>
                            </ul>
                            <button className="btn btn-primary" onClick={handleLogout}>
                                Logout
                            </button>
                        </div>
                    </div>
                </nav>
            )}
        </div>
    );
}
