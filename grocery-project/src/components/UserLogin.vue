<template>
<div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="navbar-brand">
            <span>
                User Login
            </span>
        </div>
        <div class="ml-auto">
            <button class="btn btn-outline-primary" @click="home()"> Home </button>
        </div> 
    </nav>
</div>
<br>
    <div class="container mt-5">
        <div class="form-group">
        <input type="text" v-model="username" placeholder="Username">
        </div>
        <div class="form-group">
        <input type="password" v-model="password" placeholder="Password">
        </div>
        <div class="form-group">
        <button class="btn btn-primary" @click = "login"> Log In </button>
        </div>
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
                    const response = await fetch("http://127.0.0.1:5000/user_login", {
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
                        alert('User login successful!');
                        this.$router.push({ name: 'UserDashboard', query: {username:this.username} });
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
<style scoped>
.navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        background-color: #333;
        color: white;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
        position: fixed; 
        top: 0; 
        left: 0;  
        width: 100%; 
        z-index: 1000;
        box-sizing: border-box; 
        padding-right: 15px;
}
body {
        font-family: 'Arial', sans-serif;
        background-color: #f5f5f5;
        text-align: center;
        margin-top: 50px;
}
.container {
        background-color: white;
        padding: 20px 30px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        width: 90%;
        max-width: 400px;
        margin: 0 auto;
        border-radius: 8px;
}
.form-group {
        margin-bottom: 20px;
}
.form-group label {
        display: block;
        margin-bottom: 5px;
        font-weight: 600;
}
.form-group input {
        width: 100%;
        padding: 10px 15px;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 16px;
        box-sizing: border-box;
}
.form-check-label {
        display: flex;
        align-items: left;
}
</style>