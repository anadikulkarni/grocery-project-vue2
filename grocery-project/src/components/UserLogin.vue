<template>
    <div class="user-login-page">
        <input type="text" v-model="username" placeholder="Username">
        <input type="password" v-model="password" placeholder="Password">
        <button @click = "login"> Log In </button>
    </div>
    </template>
    <script>
    export default{
        data(){
            return{
                username: '',
                password: ''
            };
        },
        methods:{
            login(){
                console.log('user logged in')
            }
        }
    }
    </script>
    <style>
    
    </style>