import { React } from "react";
import NavBarHome from "./NavBarHome";
import NavBarSeller from "./NavBarSeller";
import NavBarBuyer from "./NavBarBuyer";
import { useLocation } from "react-router-dom";

export default function NavBar() {
    let location = useLocation();

    return (
        <div>
            {<NavBarHome />}
            {location.pathname === "/seller" && <NavBarSeller />}
            {location.pathname === "/buyer" && <NavBarBuyer />}
        </div>
    );
}
