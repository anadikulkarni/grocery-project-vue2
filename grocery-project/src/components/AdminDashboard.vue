<template>
<div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="navbar-brand">
            <span> {{ adminUsername }}'s Dashboard </span>
        </div>
        <div class="ml-auto">
            <button class="btn btn-outline-primary" @click="logout()"> Logout </button>
        </div> 
    </nav>
</div>
<br>
<div class="container mt-5">
      <button class="btn btn-primary mb-3 position-relative" @click="showRequests = !showRequests">
        Pending Requests
        <span class="badge-number">{{ numberOfPendingRequests }}</span>
      </button>
      <div v-if="showRequests">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Username</th>
              <th>Category</th>
              <th>Action</th>
              <th>Approve Request</th>
              <th>Decline Request</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in requests" :key="request.id">
              <td>{{ request.username }}</td>
              <td>{{ request.category }}</td>
              <td>{{ request.action }}</td>
              <td><button class="btn btn-success" @click="approveRequest(request.id)">Approve</button></td>
              <td><button class="btn btn-danger" @click="declineRequest(request.id)">Decline</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div id="categories-container" class="container mt-3">
      <div v-for="category in categories" :key="category.id" class="category-div" :id="category.id">
        <h2>{{ category.name }}</h2>
        <button class="btn btn-warning" @click="showEditCategoryPopup(category.id)">Edit</button> &nbsp;&nbsp;&nbsp;
        <button class="btn btn-danger" @click="deleteCategory(category.id)">Delete</button>
      </div>
      <button id="openBtn" class="btn btn-primary" @click="showCreateCategoryPopup()">Create Category</button>
    </div>
  <div v-if="isCreateCategoryVisible" id="create-category-overlay">
    <div id="create-category-popup">
      <button class="close-btn" @click="isCreateCategoryVisible = false">&times;</button>
      <input type="text" v-model="newCategoryName" placeholder="Create a category">
      <br>
      <button id="saveBtn" class="btn btn-primary" @click="saveCategory">Save</button>
    </div>
  </div>
  <div v-if="isEditCategoryVisible" id="edit-category-overlay">
    <div id="edit-category-popup">
      <button class="close-btn" @click="isEditCategoryVisible = false">&times;</button>
      <input type="hidden" v-model="categoryId" id="editing-category-id-hidden" name="category_name">
      <input type="text" id="new-category-name" placeholder="Edit category name">
      <br>
      <button id="updateBtn" class="btn btn-primary" @click="updateCategory">Update</button>
    </div>
  </div>
</template>

<script>
export default{
    data(){
        return{
            requests:[], 
            showRequests: false,
            adminUsername: '',
            categories: [],
            isCreateCategoryVisible: false,
            isEditCategoryVisible: false,
            newCategoryName: '',
            categoryID: null,
            numberOfPendingRequests: 0,
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
                this.numberOfPendingRequests = this.requests.length;
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

<style scoped>
    body{
        font-family: 'Playfair', serif;
    }
    table {
      width: 50%;
      border-collapse: collapse;
      margin: auto;
    }
    
    th, td {
      padding: 0px;
      text-align: center;
    }
    .badge-number {
      position: absolute;
      top: -10px; /* Adjust these values as needed */
      right: -10px;
      width: 20px; /* Badge size */
      height: 20px;
      background-color: red;
      color: white;
      border-radius: 50%; /* Circular shape */
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 12px; /* Font size of the number */
    }

          #create-category-overlay, #edit-category-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.5);
      z-index: 1;
    }

/* Popup Styles */
      #create-category-popup, #edit-category-popup {
        position: relative;
        top: 50%;
        left: 50%;
        width: 300px;
        padding: 20px;
        transform: translate(-50%, -50%);
        background-color: #fff;
        text-align: center;
        border-radius: 10px;
      }

      /* Close Button Styles */
      .close-btn {
        position: absolute;
        top: 10px;
        right: 10px;
        border: none;
        background-color: transparent;
        cursor: pointer;
        font-size: 20px;
      }

      /* Input and Button Spacing */
      input[type="text"] {
        margin-bottom: 15px; /* Add margin to create space */
      }

      #categories-container {
          display: flex;
          align-items: left;
          justify-content: center;
          flex-wrap: wrap;
      }

      .category-div {
          width: 300px; 
          height: 140px; 
          margin: 60px auto; 
          box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1), 0px 6px 20px rgba(0, 0, 0, 0.13); 
          overflow-y: auto; 
          padding: 20px;
          border-radius: 8px; 
          background-color: #ffffff;
          text-align: center;
          vertical-align: top;
          position: relative;
      }

      /* #edit-category-overlay {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-color: rgba(0, 0, 0, 0.5);
          z-index: 1;
      }

      #edit-category-popup {
          position: relative;
          top: 50%;
          left: 50%;
          width: 300px;
          padding: 20px;
          transform: translate(-50%, -50%);
          background-color: #fff;
          text-align: center;
          border-radius: 10px;
      } */

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
      #admin-username {
          margin-right: 20px;
          font-weight: bold;
      }

      .navbar button {
          margin-left: 10px;
          padding: 5px 15px;
          background-color: #555;
          color: white;
          border: none;
          cursor: pointer;
          transition: background-color 0.3s;
      }

      .navbar button:hover {
          background-color: #777;
      }
      #openBtn {
          position: fixed;  
          bottom: 20px;       
          right: 20px;      
          background-color: #008CBA; 
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 50px; 
          font-size: 16px;
          cursor: pointer;
          transition: background-color 0.3s ease-in-out;
          z-index: 1000;  
      }

      #openBtn:hover {
          background-color: #006c99;
      }

      .category-div button.add-btn {
          background-color: #008CBA; 
          color: white;
          border: none;
          border-radius: 50%;
          width: 40px;
          height: 40px;
          position: relative;
          margin-top: 10px;
      }

      .category-div button.add-btn:hover {
          cursor: pointer;
      }

      .category-div button.add-btn::before {
          content: '+';
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          font-weight: bold;
      }

      .category-div button.edit-btn, .category-div button.delete-btn {
          width: 80px; 
          height: 35px; 
          line-height: 35px; 
          border: none;
          border-radius: 15px; 
          display: inline-block; 
          font-size: 14px;
          text-align: center;
          margin-top: 10px;
          position: absolute; 
          bottom: 10px;
      }

      .category-div button.edit-btn, .category-div button.delete-btn:hover {
          cursor: pointer;
      }
</style>