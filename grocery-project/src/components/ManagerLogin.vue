<template>
    <div class="manager-login-page">
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
                console.log('manager logged in')
            }
        }
    }
    </script>
    <style>
    
    </style>