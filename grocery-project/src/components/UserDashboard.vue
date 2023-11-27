<template>
    <div>
    <nav class="navbar">
        <div class="navbar-left">
            <span id="username">{{ user }}'s dashboard </span>
        </div>
        <div class="navbar-right">
            <button @click="goToCart()"> Cart </button>
            <button @click="logout()"> Logout </button>
        </div>
    </nav>
    </div>
    <div class="filter-button-container">
        <button @click="showFilterPopup()"> Search </button>
    </div>
    <div v-if="filterPopupVisible" class="popup">
        <div class="popup-content">
            <span class="close-button" @click="closeFilterPopup()"> &times; </span>
            <h3> Product Search </h3>
            <div class="popup-input">
                <label for="category-select"> Categories: </label>
                <div v-for="category in categories" :key="category.name" class="category-checkbox">
                    <input type="checkbox" :value="category.name" v-model="selectedCategories">
                    <span> {{ category.name }} </span>
                </div>
            </div>
            <div class="popup-input">
                <label for="min-price"> Min Price: </label>
                <input type="number" v-model="minPrice" id="min-price">
                <br>
                <label for="max-price"> Max Price: </label>
                <input type="number" v-model="maxPrice" id="max-price">
            </div>
            <div class="popup-input">
                <label for="mfd-date-min"> Manufactured After Date: </label>
                <input type="date" id="mfd-date-min" v-model="mfdDateMin">
            </div>
            <button @click="applyFilters()"> Search </button>
        </div>
    </div>
    <div class="container">
        <div v-for="category in filteredCategories" :key="category.name" class="category-block">
            <h2> {{ category.name }} </h2>
            <div v-for="product in category.products" :key="product.id" class="product-block">
                <div class="product-info">
                    <span> {{ product.productName }} </span>
                    <span class="product-price"> {{ product.rateUnit }}/{{ product.unit }} </span>
                    <span class="product-quantity"> Quantity Available: {{ product.quantity }}</span>
                </div>
                <div class="product-actions">
                    <button v-if="product.quantity > 0" class="buy-btn" @click="showBuyPopup(product.rateUnit,product.id)"> Buy </button>
                    <button v-if="product.quantity > 0" class="cart-btn" @click="showCartPopup(product.rateUnit,product.id)"> Add to Cart</button>
                    <label v-else class="out-of-stock"> Out of Stock</label>
                </div>
            </div>
        </div>
    </div>
    <div v-if="buyPopupVisible" id="buy-popup" class="popup">
        <div class="popup-content">
            <span class="close-button" @click="hideBuyPopup()"> &times; </span>
            <h3> Buy a Product </h3>
            <div class="popup-input">
                <label for="product-quantity"> Quantity: </label>
                <input v-model.number="buyQuantity" type="number" id="product-quantity" @change="updateTotalPrice()">
            </div>
            <div class="popup-price">
                Total Price: &#8377;<span id="total-price">{{ buyTotalPrice }}</span>
            </div>
            <button @click="finalizePurchase()"> Buy </button>
        </div>
    </div>
    <div v-if="cartPopupVisible" id="add-to-cart-popup" class="popup">
        <div class="popup-content">
            <span class="close-button" @click="hideCartPopup()"> &times; </span>
            <h3> Add to Cart </h3>
            <div class="popup-input">
                <label for="product-quantity"> Quantity: </label>
                <input v-model.number="cartQuantity" type="number" id="add-to-cart-product-quantity" @change="addToCartUpdateTotalPrice()">
            </div>
            <div class="popup-price">
                Total Price: &#8377;<span id="add-to-cart-total-price">{{ cartTotalPrice }}</span>
            </div>
            <button @click="finalizeAddToCart()"> Add to Cart </button>
        </div>
    </div>
</template>
<script>
export default{
    data(){
        return{
            user: '',
            categories: [],
            isCreateCategoryVisible: false,
            isEditCategoryVisible: false,
            isCreateProductVisible: false,
            isEditProductVisible: false,
            newCategoryName: '',
            categoryID: null,
            cartPopupVisible: false,
            buyPopupVisible: false,
            filterPopupVisible: false,
            cartQuantity: 1,
            selectedProductID: '',
            selectedProductRate: 0,
            selectedCategories: [],
            cartTotalPrice: 0,
            buyTotalPrice: 0,
            buyQuantity: 1,
            priceRange: [0,1000],
            minPrice: null,
            maxPrice: null,
            mfdDateMin: null,
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
    computed: {
        filteredCategories(){
            const isFilterActive = this.selectedCategories.length > 0 || this.minPrice != null || this.maxPrice != null || this.mfdDateMin != null;
            return this.categories.filter(category => (this.selectedCategories.length === 0 || this.selectedCategories.includes(category.name)))
            .map(category => ({...category,
                                products:category.products.filter(product => 
                                (!isFilterActive || (
                                    (this.minPrice === null || product.rateUnit >= this.minPrice) &&
                                    (this.maxPrice === null || product.rateUnit <= this.maxPrice) &&
                                    (!this.mfdDateMin || new Date(product.mfd) >= new Date(this.mfdDateMin))
                                    )))}))
            .filter(category => category.products.length > 0);
        }
    },
    methods: {
        async fetchUserAndCategories(){
            try {
                let response = await fetch(`http://127.0.0.1:5000/categories_user?username=${this.$route.query.username}`,{
                    method: 'GET',
                    credentials: 'include',
                });
                if(response.status === 401 || response.status === 404){
                    this.$router.push({name: 'UserLogin'});
                }
                let data = await response.json();
                this.categories = data.categories;
                this.user = data.user;
        } catch (error) {
                console.error("Error fetching categories and products:", error);
            }
        },
        applyFilters(){
            this.closeFilterPopup();
        },
        goToCart(){
            this.$router.push({
                name: 'UserCart',
                query: {username: this.user},
            });
        },
        async logout(){
            await fetch(`http://127.0.0.1:5000/logout?username=${this.$route.query.username}`,{
                    method: 'GET',
                    credentials: 'include',
                });
            this.$router.push({name: "HomePage"});
        },
        showCartPopup(rateUnit, productID){
            this.selectedProductID = productID;
            this.cartPopupVisible = true;
            this.selectedProductRate = rateUnit;
            this.cartTotalPrice = rateUnit;
        },
        showBuyPopup(rateUnit, productID){
            this.selectedProductID = productID;
            this.buyPopupVisible = true;
            this.selectedProductRate = rateUnit;
            this.buyTotalPrice = rateUnit;
        },
        hideCartPopup(){
            this.cartPopupVisible = false;
        },
        hideBuyPopup(){
            this.buyPopupVisible = false;
        },
        showFilterPopup(){
            this.filterPopupVisible = true;
        },
        closeFilterPopup(){
            this.filterPopupVisible = false;
        },
        addToCartUpdateTotalPrice(){
            if(this.cartQuantity >= 0){
                this.cartTotalPrice = this.cartQuantity * this.selectedProductRate.toFixed(2);
            }
            else{
                alert('Quantity cannot be negative');
                this.cartQuantity = 0;
                this.cartTotalPrice = this.cartQuantity * this.selectedProductRate.toFixed(2);
            }
        },
        async finalizeAddToCart(){
            try{
                const response = await fetch("http://127.0.0.1:5000/add_to_cart_product",{
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                      "productID": this.selectedProductID,
                      "quantity": this.cartQuantity,
                      "username": this.user,
                  })
                });
                const data = await response.json();
                if(data.status == 'success'){
                    alert(data.message);
                    window.location.reload();
                }
                else{
                    console.log('error adding to cart:', data.message);
                }
                }
            catch(error){
                console.error('error adding to cart: ', error);
            }
                
            this.hideCartPopup();
        },
        updateTotalPrice(){
            if(this.buyQuantity >= 0){
                this.buyTotalPrice = (this.selectedProductRate*this.buyQuantity).toFixed(2);
            }
            else{
                alert('Quantity cannot be negative');
                this.buyQuantity = 0;
                this.buyTotalPrice = (this.selectedProductRate*this.buyQuantity).toFixed(2);
            }
        },
        async finalizePurchase(){
            try{
                const response = await fetch("http://127.0.0.1:5000/purchase_product",{
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                      "productID": this.selectedProductID,
                      "quantity": this.buyQuantity,
                      "username": this.user,
                  })
                });
                const data = await response.json();
                if(data.status == 'success'){
                    alert(data.message);
                    window.location.reload();
                }
                else{
                    console.log('error purchasing product:', data.message);
                }
                }
            catch(error){
                console.error('error purchasing product: ', error);
            }
                
            this.hideBuyPopup();
        }
    },
    mounted(){
        this.fetchUserAndCategories();
    }
}
</script>

<style>
body {
            font-family: 'Playfair', serif;
            padding-top: 60px;
        }
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            background-color: #333;
            color: white;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
            font-family: 'Playfair', serif;
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
        .container {
            width: 80%;
            margin: 20px auto;
            font-family: Arial, sans-serif;
        }
        .category-block {
            background-color: #e6f7ff;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
            font-family: 'Playfair', serif;
        }
        .product-block {
            background-color: #fffae6;
            padding: 10px;
            margin-top: 10px;
            border-radius: 5px;
            font-family: 'Playfair', serif;
        }
        .product-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: 'Playfair', serif;
        }
        .product-price {
            margin-left: 10px;
            color: #444;
            font-weight: bold;
            font-family: 'Playfair', serif;
        }
        .product-actions {
            display: flex;
            justify-content: right;
            align-items: center;
            gap: 10px;
            margin-top: 10px;
        }
        .buy-btn, .cart-btn {
            padding: 5px 15px;
            cursor: pointer;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-family: 'Playfair', serif;
        }
        .buy-btn {
            background-color: #4CAF50;
            color: white;
        }
        .cart-btn {
            background-color: #FFC107;
            color: white;
        }
        .popup {
            position: fixed; 
            top: 0; 
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.7);
            z-index: 1000;
        }
        .popup-content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #fff;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
            width: 300px;
            border-radius: 5px;
        }
        .close-btn {
            cursor: pointer;
            float: right;
            font-size: 28px;
            font-weight: bold;
            font-family: 'Playfair', serif;
        }
        .popup-input, .popup-price {
            margin: 20px 0;
        }
        #manager-username {
            margin-right: 20px;
            font-weight: bold;
            font-family: 'Playfair', serif;
        }
</style>