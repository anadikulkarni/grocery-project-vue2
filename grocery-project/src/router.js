import {createRouter, createWebHistory} from "vue-router"
import Home from "./components/Home.vue"
import Register from "./components/RegisterPage.vue"
import AdminLogin from "./components/AdminLogin.vue"
import ManagerLogin from "./components/ManagerLogin.vue"
import UserLogin from "./components/UserLogin.vue"
import AdminDashboard from "./components/AdminDashboard.vue"
import ManagerDashboard from "./components/ManagerDashboard.vue"
import UserDashboard from "./components/UserDashboard.vue"
import UserCart from "./components/UserCart.vue"

const routes = [
    {
        path: "/",
        name: "HomePage",
        component: Home,
    },
    {
        path: "/register",
        name: "RegisterPage",
        component: Register,
    },
    {
        path: "/adminlogin",
        name: "AdminLogin",
        component: AdminLogin,
    },
    {
        path: "/managerlogin",
        name: "ManagerLogin",
        component: ManagerLogin,
    },
    {
        path: "/userlogin",
        name: "UserLogin",
        component: UserLogin,
    },
    {
        path: "/admindashboard",
        name: "AdminDashboard",
        component: AdminDashboard,
    },
    {
        path: "/managerdashboard",
        name: "ManagerDashboard",
        component: ManagerDashboard,
    },
    {
        path: "/userdashboard",
        name: "UserDashboard",
        component: UserDashboard,
    },
    {
        path: "/user_cart",
        name: "UserCart",
        component: UserCart,
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
