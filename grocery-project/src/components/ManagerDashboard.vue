<template>
<div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="navbar-brand">
            <span> {{ managerUsername }}'s Dashboard </span>
        </div>
        <div class="ml-auto">
            <button class="btn btn-outline-primary" @click="logout()"> Logout </button>
        </div> 
    </nav>
</div>
<br>
    <button class="btn btn-primary mb-3 position-relative" @click="exportProductAsCSV()"> Export Product Information </button>
    <div id="categories-container">
        <div v-for="category in categories" :key="category.id" class="category-div" :id="category.id">
            <h2> {{category.name}} </h2>
            <div class="products-container">
                <div v-for="product in category.products" :key="product.id" class="product-div" :id="'product-'+product.id">
                    <span> {{product.productName}} </span>
                    <button @click="showEditProductPopup(product.id, product.productName, product.unit, product.rateUnit, product.quantity)"> Edit </button>
                    <button @click="deleteProduct(product.id)"> Delete </button>
                </div>
            </div> 
            <button @click="showCreateProductPopup(category.id)" class="add-btn">    
            </button> <br> <br>
            <button @click="showEditCategoryPopup(category.id)" class="btn btn-warning"> Edit </button> &nbsp;&nbsp;
            <button @click="deleteCategory(category.id)" class="btn btn-danger"> Delete </button>
        </div>
    </div>
    <div v-if="isCreateProductVisible" id="add-product-overlay">
    <div id="add-product-popup">
        <h3> Add Product </h3>
        <form id="add-product-form">
            <input type="hidden" v-model="categoryID" id="category-id-hidden" name="categoryID">
            <span class="close-button" @click="hideCreateProductPopup()"> &times; </span>
            <input type="text" name="Product Name" placeholder="grocery item" required id="productName">
            <select name="Unit" required id="unit"> 
                <option value=""> Select a Unit: </option>
                <option value="kg"> kilogram </option>
                <option value="L"> litre </option>
                <option value="dz"> dozen </option>
                <option value="g"> gram </option>
            </select>
            <input type="number" name="Rate/Unit" placeholder="Rs:" required id="rate-unit">
            <input type="number" name="Quantity" placeholder="number of items" required id="quantity">
            <input type="date" name="Manufacture Date" required id="mfd"> <br>
            <button type="button" class="btn btn-primary" id="addProductSubmit" @click="saveProduct()"> Submit </button>
        </form>
    </div>
    </div>
    <div id="edit-product-overlay" v-if="isEditProductVisible">
        <div id="edit-product-popup">
            <h3> Edit Product </h3>
            <form id="edit-product-form">
                <input type="hidden" id="edit-product-id-hidden" v-model="productId">
                <span class="close-button" @click="hideEditProductPopup()"> &times; </span>
                <input type="text" name="Product Name" placeholder="grocery item" required id="edit-productName" v-model="productName">
                <select name="Unit" required id="edit-unit" v-model="productUnit"> <!-- not properly showing up -->
                    <option value=""> Select a Unit: </option>
                    <option value="kg"> kilogram </option>
                    <option value="L"> litre </option>
                    <option value="dz"> dozen </option>
                    <option value="g"> gram </option>
                </select>
                <input type="number" name="Rate/Unit" placeholder="Rs:" required id="edit-rate-unit" v-model="productRate">
                <input type="number" name="Quantity" placeholder="number of items" required id="edit-quantity" v-model="productQuantity">
                <input type="date" name="Manufacture Date" required id="edit-mfd">
                <button type="button" class="btn btn-primary" id="edit-productSubmit" @click="editProduct()"> Submit </button>
            </form>
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
</template>

<script>
export default{
    data(){
        return{
            managerUsername: '',
            categories: [],
            isCreateCategoryVisible: false,
            isEditCategoryVisible: false,
            isCreateProductVisible: false,
            isEditProductVisible: false,
            newCategoryName: '',
            categoryID: null,
            product: {
                categoryID: '',
                productId: '',
                productName: '',
                unit: '',
                rateUnit: '',
                quantity: '',
                mfd: '',
            },
            editingCategory: {
                id: null,
                name: '',
            },
            productId: '',
            productName: '',
            productUnit: '',
            productRate: '',
            productQuantity: '',
            productMfd: '',

        }
    },
    methods: {
        async fetchUserAndCategories(){
        try {
                let response = await fetch(`http://127.0.0.1:5000/categories?username=${this.$route.query.username}`,{
                    method: 'GET',
                    credentials: 'include',
                });
                if(response.status === 401 || response.status === 404){
                    this.$router.push({name: 'ManagerLogin'});
                }
                let data = await response.json();
                this.categories = data.categories;
                this.managerUsername = data.manager;
                console.log(data);
        } catch (error) {
                console.error("Error fetching pending requests:", error);
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
        showCreateProductPopup(categoryId){
            this.isCreateProductVisible = true;
            this.categoryID = categoryId;
        },
        hideCreateProductPopup(){
            this.isCreateProductVisible = false;
        },
        showEditProductPopup(productId, productName, productUnit, productRate, productQuantity, productMfd){
            this.productId = productId;
            this.productName = productName;
            this.productUnit = productUnit;
            this.productRate = productRate;
            this.productQuantity = productQuantity;
            this.productMfd = productMfd;
            this.isEditProductVisible = true;
        },
        hideEditProductPopup(){
            this.isEditProductVisible = false;
        },
        async saveCategory(){
            try{
                const response = await fetch("http://127.0.0.1:5000/create_category_request",{
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                      "category": this.newCategoryName,
                      "username": this.managerUsername,
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
        async saveProduct(){
            this.product.categoryid = document.getElementById("category-id-hidden").value;
            this.product.productName = document.getElementById("productName").value;
            this.product.unit = document.getElementById("unit").value;
            this.product.rateUnit = parseFloat(document.getElementById("rate-unit").value);
            this.product.quantity = parseInt(document.getElementById("quantity").value);
            this.product.mfd = document.getElementById("mfd").value;
            
            fetch('http://127.0.0.1:5000/save_product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.product)
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    alert('Product saved successfully!');
                    window.location.reload();
                } else {
                    alert('Error saving product!');
                }
            })
            .catch(error => {
                console.error("There was an error saving the product:", error);
            });
            this.hideCreateProductPopup();
        },
        async editProduct(){
            this.product.productId = document.getElementById("edit-product-id-hidden").value;
            this.product.productName = document.getElementById("edit-productName").value;
            this.product.unit = document.getElementById("edit-unit").value;
            this.product.rateUnit = parseFloat(document.getElementById("edit-rate-unit").value);
            this.product.quantity = parseInt(document.getElementById("edit-quantity").value);
            this.product.mfd = document.getElementById("edit-mfd").value;
            
            fetch('http://127.0.0.1:5000/edit_product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.product)
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    alert('Product saved successfully!');
                } else {
                    alert('Error saving product!');
                }
            })
            .catch(error => {
                console.error("There was an error saving the product:", error);
            });
            this.hideEditProductPopup();
        },
        async updateCategory(){
            this.editingCategory.id = document.getElementById("edit-category-id-hidden").value;
            this.editingCategory.name = document.getElementById("edit-categoryName").value;
            
            fetch('http://127.0.0.1:5000/edit_category_request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'category': this.editingCategory.name,
                    'username': this.managerUsername,
                    'categoryID': this.editingCategory.id,
                })
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    alert(data.message);
                    window.location.reload();
                } else {
                    alert('Error updating category!');
                }
            })
            .catch(error => {
                console.error("There was an error saving the category:", error);
            });
            this.hideEditCategoryPopup();
        },
        async deleteProduct(productID){
            
            fetch('http://127.0.0.1:5000/delete_product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({"productID":productID})
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    alert('Product deleted successfully!');
                    window.location.reload();
                } else {
                    alert('Error deleting product!');
                }
            })
            .catch(error => {
                console.error("There was an error deleting the product:", error);
            });
        },
        async deleteCategory(categoryID){
            
            fetch('http://127.0.0.1:5000/delete_category_request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'username': this.managerUsername,
                    'categoryID': categoryID,
                })
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    alert('Category delete request sent successfully!');
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
        async exportProductAsCSV(){
            await fetch(`http://127.0.0.1:5000/export_csv?username=${this.$route.query.username}`,{
                    method: 'GET',
                    credentials: 'include',
                })
            .then(response => response.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const tempA = document.createElement("a");
                tempA.style.display = "none";
                tempA.href = url;
                tempA.download = 'product_export_table.csv';
                document.body.appendChild(tempA);
                tempA.click();
                window.URL.revokeObjectURL(url);
            })
            .catch(() => alert('There was an error in downloading your file'));
        },
    },
    mounted(){
        this.fetchUserAndCategories();
    }
}
</script>

<style scoped>
body {
            font-family: 'Playfair', serif;
        }
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
        .navbar-left, .navbar-right {
            display: flex;
            align-items: center;
        }
        #manager-username {
            margin-right: 20px;
            font-weight: bold;
        }
        .navbar button {
            margin-left: 10px;
            padding: 5px 15px;
            background-color: #999;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
            font-family: 'Playfair', serif;
        }
        .navbar button:hover {
            background-color: #777;
        }
        #add_cat {
            position: fixed;  
            bottom: 30px;       
            right: 30px;      
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
        #add_cat:hover {
            background-color: #006c99;
        }
        .category-div {
            width: 300px; 
            height: 400px; 
            margin: 60px auto; 
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1), 0px 6px 20px rgba(0, 0, 0, 0.13); 
            overflow-y: auto; 
            padding: 20px;
            border-radius: 30px; 
            background-color: #ffffff;
            vertical-align: top;
            text-align: center;
            position: relative;
        }
        #categories-container {
            display: flex;
            align-items: center;
            justify-content: center;
            flex-wrap: wrap;
        }
        #overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1;
        }
        #popup {
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
        #edit-category-overlay {
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
        }
        #add-product-overlay{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1;
        }
        #edit-product-overlay{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1;
        }
        #add-product-popup{
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
        #edit-product-popup{
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
        .category-div button.add-btn:hover{
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
        .category-div button.edit-btn:hover{
            cursor: pointer;
        }
        .category-div button.delete-btn:hover{
            cursor: pointer;
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
            bottom: 10px; /* distance from the bottom */
        }
        .category-div button.edit-btn {
            background-color: #ffeb85; 
            /* margin-right: 10px; */
            left: 85px;
        }
        .category-div button.delete-btn {
            background-color: #ffb3b3; 
            right: 85px;
        }
        .products-container {
            height: 55%;
            overflow-y: auto; 
            padding: 10px; 
            border-radius: 5px; 
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); 
        }
        .product-div {
            display: flex; 
            justify-content: space-between;
            align-items: center;
            padding: 10px; 
            border-bottom: 1px solid #e1e1e1;
        }
        .product-div:last-child {
            border-bottom: none;
        }
        .product-div span {
            flex: 1;
            font-size: 14px;
            font-family: 'Playfair', serif;
            text-align: left;
            margin-right: 10px;
        }
        .product-div button {
            margin: 0 5px;
            padding: 5px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            font-family: 'Playfair', serif;
        }
        .product-div button:hover {
            opacity: 0.8;
        }
        .product-div button:nth-child(2) {
            background-color: #d1ffd1;
        }
        .product-div button:nth-child(3) {
            background-color: #ffc1c1;
        }
</style>