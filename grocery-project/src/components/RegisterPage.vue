<template>
<div>
    <nav class="navbar">
        <div class="navbar-right">
            <button @click="home()"> Home </button>
        </div>
    </nav>
</div>
<div class="register-page">
    <input type="text" v-model="username" placeholder="Username">
    <input type="password" v-model="password" placeholder="Password">
    <input type="email" v-model="email" placeholder="Email">
    <input type="checkbox" v-model="isManager" id="managerCheckbox">
    <label for = "managerCheckbox"> Register as Manager? </label>
    <button @click = "register"> Register </button>
</div>
</template>
<script>
export default{
    data(){
        return{
            username: '',
            password: '',
            email: '',
            isManager: false
        };
    },
    methods:{
        async register() {
        if(this.isManager) {
          console.log('Manager registered:', this.username, 'Manager password', this.password);
        } else {
          console.log('User registered:', this.username, 'User password', this.password);
        }
        try {
            let response = await fetch("http://127.0.0.1:5000/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: 'include',
                body: JSON.stringify({
                    username: this.username,
                    password: this.password,
                    email: this.email,
                    isManager: this.isManager
                })
            });

            let data = await response.json();
            alert(data.message);

        } catch (error) {
            console.error("There was an error during registration:", error);
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