import { React } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function NavBarSeller() {
    let navigate = useNavigate();

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
