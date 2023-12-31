import React, { useState } from "react";
import "./Navbar.css"
import { MenuList } from "./MenuList";
import { NavLink } from "react-router-dom";

const Navbar = () => {
    const [clicked, setClicked] = useState(false);

    const menuList = MenuList.map(({ title, url }, index) => {
        return (
            <li key={index}>
                {/* <a href={url}>{title}</a> */}
                <NavLink to={url} activeClassName="active">{title}</NavLink>
            </li>
        )
    });

    return (
        <nav>
            <div className="logo">
                VPN<font>Lab</font>
            </div>
            <div className="menu-icon" onClick={() => setClicked(!clicked)}>
                <i className={clicked ? "fas fa-times" : "fa fa-bars"}></i>
            </div>
            <ul className={clicked ? "menu-list" : "menu-list close"}>
                {menuList}
            </ul>
        </nav>
    );
}

export default Navbar;