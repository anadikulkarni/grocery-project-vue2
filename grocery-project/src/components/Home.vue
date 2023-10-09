<template>
<div class='homepage'>
    <router-link to = "/register">
    <button> Register </button>
    </router-link>
    <router-link to = "/adminlogin">
    <button> Admin Login </button>
    </router-link>
    <router-link to = "/managerlogin">
    <button> Manager Login </button>
    </router-link>
    <router-link to = "/userlogin">
    <button> User Login </button>
    </router-link>
</div>
</template>

<script>
export default{
    name: "HomePage",
    methods: {
        loginAdmin(){
            console.log('admin logged in')
        },
        loginManager(){
            console.log('manager logged in')
        },
        loginUser(){
            console.log('user logged in')
        }
    }
}
</script>

<style>

</style>