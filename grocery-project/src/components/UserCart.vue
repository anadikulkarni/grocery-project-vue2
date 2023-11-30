<template>
<div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="navbar-brand">
            <span id="username"> {{ username }}'s Cart </span>
        </div>
        <div class="ml-auto">
            <button class="btn btn-outline-primary" @click="goToDashboard()"> Dashboard </button>
            <button class="btn btn-outline-primary" @click="logout()"> Logout </button>
        </div> 
    </nav>
</div>
<br>
    <!-- <div id="cart-container">
        <input type="hidden" id="hidden-user-id" :value="userID">
        <div class="cart-item" v-for="item in items" :key="item.ID">
        <span> {{item.category}} - {{item.productName}} </span>
        <span> {{item.quantity}} {{item.unit}} </span>
        <span> &#8377;{{item.rateUnit}}/{{item.unit}} </span>
        <span class="item-total" :data-item-total="item.quantity*item.rateUnit"> Total: &#8377;{{item.quantity*item.rateUnit}}</span>
        <button class="remove-button" @click="removeItem(item.id)"> Remove </button>
        </div>
    </div> -->
    <div id="cart-container">
        <input type="hidden" id="hidden-user-id" :value="userID">
        <table class="table">
            <thead>
                <tr>
                    <th> Product - Category </th>
                    <th> Quantity </th>
                    <th> Price/Unit </th>
                    <th> Total </th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in items" :key="item.ID">
                    <td> {{item.category}} - {{item.productName}} </td>
                    <td> {{item.quantity}} {{item.unit}} </td>
                    <td> &#8377;{{item.rateUnit}}/{{item.unit}} </td>
                    <td> <span :data-item-total="item.quantity*item.rateUnit"> Total: &#8377;{{item.quantity*item.rateUnit}}</span> </td>
                    <td> <button class="remove-button" @click="removeItem(item.id)"> Remove </button> </td>
                </tr>
                <tr>
                    <td> </td>
                    <td></td>
                    <td> </td>
                    <td><span class="grand-total-display"> Grand Total: &#8377;{{ grandTotal }} </span></td>
                    <td> <button class="btn btn-primary" @click="buyAll()"> Buy All </button></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
<script>
    export default{
        data(){
            return{
                username: '',
                userID: '',
                items: [],
                grandTotal: '',
            };
        },
        methods:{
            async getDataAndCalculateGrandTotal(){
                try {
                let response = await fetch(`http://127.0.0.1:5000/cart?username=${this.$route.query.username}`,{
                    method: 'GET',
                    credentials: 'include',
                });
                if(response.status === 401 || response.status === 404){
                    this.$router.push({name: 'UserLogin'});
                }
                let data = await response.json();
                this.items = data.items;
                this.username = data.user;
        } catch (error) {
                console.error("Error fetching pending requests:", error);
            }
            this.grandTotal = this.items.reduce((total, item)=>total+(item.rateUnit*item.quantity),0);
        },
        goToDashboard(){
            this.$router.push({
                name: 'UserDashboard',
                query: {username: this.username},
            });
        },
        async logout(){
            await fetch(`http://127.0.0.1:5000/logout?username=${this.$route.query.username}`,{
                    method: 'GET',
                    credentials: 'include',
                });
            this.$router.push({name: "HomePage"});
        },
        removeItem(itemID){
            fetch(`http://127.0.0.1:5000/remove_item`,{
                method: 'POST',
                credentials: 'include',
                body: JSON.stringify({
                    'itemID': itemID,
                }),
                headers: {'Content-Type': 'application/json'},
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                location.reload();
            })
            .catch(error => {
                alert(error);
            })
        },
        async buyAll(){
            try{
                const response = await fetch("http://127.0.0.1:5000/buy_all",{
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                      "userID": this.username,
                  })
                });
                const data = await response.json();
                if(data.status == 'success'){
                    alert(data.message);
                    window.location.reload();
                }
                else{
                    console.log('error purchasing products:', data.message);
                }
                }
            catch(error){
                console.error('error purchasing products: ', error);
            }
        },
    },
        mounted(){
            this.getDataAndCalculateGrandTotal();
        },
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
        #manager-username {
            margin-right: 20px;
            font-weight: bold;
        }
        .cart-item {
            border: 1px solid #ddd;
            padding: 10px;
            margin: 10px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .grand-total-section {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
            padding: 10px;
            border-top: 1px solid #ddd;
        }
        .grand-total-display {
            font-weight: bold;
            font-size: 1.2em;
        }
        .buy-all-button {
            padding: 5px 15px;
            background-color: #555;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
            border-radius: 5px;
        }
        .buy-all-button:hover {
            background-color: #777;
        }
        .remove-button {
            padding: 4px 10px;
            background-color: #ffb3b3;
            border-radius: 5px;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .remove-button:hover {
            background-color: #d32f2f; /* Dark Red */
        }
</style>