import {createRouter, createWebHistory} from "vue-router"
import Home from "./components/Home.vue"
import Register from "./components/RegisterPage.vue"
import AdminLogin from "./components/AdminLogin.vue"
import ManagerLogin from "./components/ManagerLogin.vue"
import UserLogin from "./components/UserLogin.vue"

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
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
