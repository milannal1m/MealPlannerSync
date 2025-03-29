import { createRouter, createWebHistory } from 'vue-router';

import HomePage from '../pages/HomePage.vue';
import UserPage from '../pages/UserPage.vue';
import MealPage from '../pages/MealPage.vue';
import LoginPage from '../pages/LoginPage.vue';

const routes = [

    { path: '/', component: LoginPage },
    { path: '/home', component: HomePage },
    { path: '/user', component: UserPage },
    { path: '/meal', component: MealPage }
];

export default createRouter ({

    history: createWebHistory(),
    routes

});