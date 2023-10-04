<template>
<div class='homepage'>
    <button @click="register"> Register </button>
    <button @click="loginAdmin"> Admin Login </button>
    <button @click="loginManager"> Manager Login </button>
    <button @click="loginUser"> User Login </button>
</div>
</template>

<script>
export default{
    name: "HomePage",
    methods: {
        register(){
            console.log('registered')
        },
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