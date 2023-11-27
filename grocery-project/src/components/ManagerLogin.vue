<template>
<div>
    <nav class="navbar">
        <div class="navbar-right">
            <button @click="home()"> Home </button>
        </div>
    </nav>
</div>
    <div class="manager-login-page">
        <h1> Manager Login </h1>
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
            async login(){
                try{
                    const response = await fetch("http://127.0.0.1:5000/manager_login", {
                        method: 'POST',
                        headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        username: this.username,
                        password: this.password
                    })
                    });
                    const data = await response.json();
          
                    if (data.status === 'success') {
                        alert('Manager login successful!');
                        this.$router.push({ name: 'ManagerDashboard', query: {username:this.username} });
                    } else {
                        alert('Login failed!');
                    }
                    } catch (error) {
                    console.error("There was an error logging in:", error);
                    }
                },
                home(){
                this.$router.push({name: "HomePage"});
            },
            }
        }
    </script>
    <style>
    
    </style>