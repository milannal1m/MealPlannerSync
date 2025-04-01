import { createRouter, createWebHistory } from 'vue-router';

import HomePage from '../pages/HomePage.vue';
import UserPage from '../pages/UserPage.vue';
import MealPage from '../pages/MealPage.vue';
import LoginPage from '../pages/LoginPage.vue';
import AddUser from '../pages/AddUser.vue';

const routes = [

    { path: '/', component: LoginPage },
    { path: '/home', component: HomePage },
    { path: '/user', component: UserPage },
    { path: '/meal', component: MealPage },
    { path: '/adduser', component: AddUser }

];

export default createRouter ({

    history: createWebHistory(),
    routes

});