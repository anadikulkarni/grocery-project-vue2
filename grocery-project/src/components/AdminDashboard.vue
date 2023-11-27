<template>
<div>
    <nav class="navbar">
        <div class="navbar-left">
            <span id="admin-username"> {{ adminUsername }}'s Dashboard </span>
        </div>
        <div class="navbar-right">
            <button> Summary </button>
            <button @click="logout()"> Logout </button>
        </div>
    </nav>
</div>
<div>
    <button @click="showRequests = !showRequests"> Show Pending Requests </button>
    <div v-if="showRequests">
        <table>
            <thead> 
                <tr>
                 <th>Username</th>
                 <th>Category</th>
                 <th>Action</th>
                 <th>Approve </th>
                 <th>Decline </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="request in requests" :key="request.id">
                    <td> {{ request.username }}</td>
                    <td> {{  request.category }}</td>
                    <td> {{ request.action }}</td>
                    <td> <button @click="approveRequest(request.id)"> Approve </button></td>
                    <td> <button @click="declineRequest(request.id)"> X </button></td>
                </tr>
            </tbody>
        </table>
    </div>
    <div>
        <div id="categories-container">
        <div v-for="category in categories" :key="category.id" class="category-div" :id="category.id">
            <h2> {{category.name}} </h2>
            <button @click="showEditCategoryPopup(category.id)" class="edit-btn"> Edit </button>
            <button @click="deleteCategory(category.id)" class="delete-btn"> Delete </button>
        </div>
    </div>
    <button id="add_cat" @click="showCreateCategoryPopup()"> Add Category </button>
    <div id="overlay" v-if="isCreateCategoryVisible">
        <div id="popup">
            <span class="close-button" @click="hideCreateCategoryPopup()"> &times; </span>
            <input type="text" v-model="newCategoryName" id="cat_name" placeholder="category name">
            <button id="save_cat" @click="saveCategory()"> Save </button>
        </div>
    </div>
    <div v-if="isEditCategoryVisible" id="edit-category-overlay">
        <div id="edit-category-popup">
            <input type="hidden" id="edit-category-id-hidden" v-model="categoryID">
            <span class="close-button" @click="hideEditCategoryPopup()"> &times; </span>
            <input type="text" id="edit-categoryName" placeholder="change category name">
            <button @click="updateCategory()" id="category-update-button"> Update </button>
        </div>
    </div>
    </div>
</div>
</template>

<script>
export default{
    data(){
        return{
            requests:[], showRequests: false,
            adminUsername: '',
            categories: [],
            isCreateCategoryVisible: false,
            isEditCategoryVisible: false,
            newCategoryName: '',
            categoryID: null,
            editingCategory: {
                id: null,
                name: '',
            },
        };
    },
    methods: {
        async fetchPendingRequests(){
            try{
                let response = await fetch(`http://127.0.0.1:5000/pending_requests?username=${this.$route.query.username}`,{
                    method: 'GET',
                    credentials: 'include',
                });
                if(response.status === 401 || response.status === 404){
                    this.$router.push({name: 'AdminLogin'});
                }
                let data = await response.json();
                this.requests = data.requests;
                this.categories = data.categories;
                console.log(this.categories);
                this.adminUsername = data.admin;
            }
            catch(error){
                console.log(error);
            }
        },
        async approveRequest(requestId) {
        try {
          let response = await fetch(`http://127.0.0.1:5000/approve-request/${requestId}`, {
            method: "POST"
          });
          let data = await response.json();
          if (data.status === "success") {
            this.requests = this.requests.filter(request => request.id !== requestId);
            window.location.reload();
          } else {
            console.error("Error approving request:", data.message);
          }
        } catch (error) {
          console.error("Error approving request:", error);
        }
      },
      async declineRequest(requestId) {
        try {
          let response = await fetch(`http://127.0.0.1:5000/decline-request/${requestId}`, {
            method: "POST"
          });
          let data = await response.json();
          if (data.status === "success") {
            this.requests = this.requests.filter(request => request.id !== requestId);
            window.location.reload();
          } else {
            console.error("Error approving request:", data.message);
          }
        } catch (error) {
          console.error("Error approving request:", error);
        }
      },
        showCreateCategoryPopup(){
            this.isCreateCategoryVisible = true;
        },
        hideCreateCategoryPopup(){
            this.isCreateCategoryVisible = false;
        },
        showEditCategoryPopup(categoryId){
            this.categoryID = categoryId;
            this.isEditCategoryVisible = true;
        },
        hideEditCategoryPopup(){
            this.isEditCategoryVisible = false;
        },
        async saveCategory(){
            try{
                const response = await fetch("http://127.0.0.1:5000/save_category",{
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                      "category_name": this.newCategoryName,
                  })
                });
                const data = await response.json();
                if(data.status == 'success'){
                    alert(data.message);
                    window.location.reload();
                }
                else{
                    console.log('error saving category:', data.message);
                }
                }
            catch(error){
                console.error('error saving category: ', error);
            }
                
            this.hideCreateCategoryPopup();
        },
        async updateCategory(){
            this.editingCategory.id = document.getElementById("edit-category-id-hidden").value;
            this.editingCategory.name = document.getElementById("edit-categoryName").value;
            
            fetch('http://127.0.0.1:5000/update_category', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.editingCategory)
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    alert(data.message);
                    window.location.reload();
                } else {
                    alert(data.message);
                    console.log(this.editingCategory);
                }
            })
            .catch(error => {
                console.error("There was an error saving the category:", error);
            });
            this.hideEditCategoryPopup();
        },
        async deleteCategory(categoryID){
            
            fetch('http://127.0.0.1:5000/delete_category', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({"categoryID":categoryID})
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    alert('Category deleted successfully!');
                    window.location.reload();
                } else {
                    alert('Error deleting category!');
                }
            })
            .catch(error => {
                console.error("There was an error deleting the category:", error);
            });
        },
        async logout(){
            await fetch(`http://127.0.0.1:5000/logout?username=${this.$route.query.username}`,{
                    method: 'GET',
                    credentials: 'include',
                });
            this.$router.push({name: "HomePage"});
        },
    },
    mounted(){
        this.fetchPendingRequests();
    }
}
</script>

<style>

</style>