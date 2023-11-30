<template>
<div class='homepage container'>
    <div class="row justify-content-center">
        <div>
            <h1> Welcome to the grocery store! </h1>
        </div> <br>
        <div class="col-md-6">
            <router-link to = "/register" class="d-block mb-2">
            <button class="btn btn-success w-50"> Register </button>
            </router-link>
            <router-link to = "/adminlogin" class="d-block mb-2">
            <button class="btn btn-primary w-50"> Admin Login </button>
            </router-link>
            <router-link to = "/managerlogin" class="d-block mb-2">
            <button class="btn btn-primary w-50"> Manager Login </button>
            </router-link>
            <router-link to = "/userlogin" class="d-block mb-2">
            <button class="btn btn-primary w-50"> User Login </button>
            </router-link>
        </div>
    </div>
</div>
</template>
<script>
export default{
    name: "HomePage",
}
</script>
<style>
</style>